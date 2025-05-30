from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from typing import Dict, List, Any, Optional, Union

# Инициализация Flask и SQLAlchemy
app: Flask = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///transactions.db"  # Путь к SQLite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False  # Отключаем устаревшее поведение
db: SQLAlchemy = SQLAlchemy(app)


class Base(DeclarativeBase):
    """Базовый класс для декларативных моделей SQLAlchemy."""
    pass


class Transaction(db.Model):
    """Модель для представления финансовой транзакции в базе данных.

    Attributes:
        id (Mapped[int]): Уникальный идентификатор транзакции (первичный ключ).
        amount (Mapped[float]): Сумма транзакции. Не может быть None.
        category (Mapped[str]): Категория транзакции (например, "Еда", "Транспорт"). Не может быть None.
        date (Mapped[str]): Дата транзакции в формате строки. Не может быть None.
        type (Mapped[str]): Тип транзакции ("доход" или "расход"). Не может быть None.
        description (Mapped[str]): Описание транзакции. По умолчанию пустая строка.
    """
    __tablename__: str = "transactions"
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    date: Mapped[str] = mapped_column(nullable=False)
    type: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(default="")


@app.route("/api/transactions", methods=["GET"])
def get_transactions() -> jsonify:
    """Обрабатывает GET-запрос для получения списка всех транзакций.

    Returns:
        jsonify: JSON-ответ со списком всех транзакций в формате:
        [
            {
                "id": int,
                "amount": float,
                "category": str,
                "date": str,
                "type": str,
                "description": str
            },
            ...
        ]

    Examples:
        >>> GET /api/transactions
        <<< 200 OK
        <<< [{"id": 1, "amount": 100.0, "category": "Food", ...}, ...]
    """
    transactions: List[Transaction] = db.session.execute(db.select(Transaction)).scalars().all()
    return jsonify([{
        "id": t.id,
        "amount": t.amount,
        "category": t.category,
        "date": t.date,
        "type": t.type,
        "description": t.description
    } for t in transactions])


@app.route("/api/transactions", methods=["POST"])
def add_transaction() -> Union[jsonify, tuple]:
    """Обрабатывает POST-запрос для добавления новой транзакции.

    Ожидает JSON в теле запроса с обязательными полями:
    - amount: float
    - category: str
    - date: str (формат "YYYY-MM-DD")
    - type: str ("доход" или "расход")
    - description: str (опционально)

    Returns:
        Union[jsonify, tuple]: В случае успеха возвращает JSON с id новой транзакции и статусом 201.
        В случае ошибки возвращает JSON с описанием ошибки и соответствующим HTTP-кодом.

    Examples:
        >>> POST /api/transactions
        >>> {"amount": 100.0, "category": "Food", "date": "2023-01-01", "type": "расход"}
        <<< 201 Created
        <<< {"status": "success", "id": 1}
    """
    data: Dict[str, Any] = request.get_json()
    
    try:
        new_transaction: Transaction = Transaction(
            amount=data["amount"],
            category=data["category"],
            date=data["date"],
            type=data["type"],
            description=data.get("description", "")
        )
        db.session.add(new_transaction)
        db.session.commit()
        return jsonify({"status": "success", "id": new_transaction.id}), 201
    except KeyError as e:
        return jsonify({"error": f"Missing required field: {str(e)}"}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@app.route("/api/transactions", methods=["DELETE"])
def delete_transactions() -> Union[jsonify, tuple]:
    """Обрабатывает DELETE-запрос для удаления транзакций по критериям.

    Ожидает JSON в теле запроса с обязательными полями:
    - category: str
    - date: str
    - type: str

    Удаляет все транзакции, соответствующие указанным критериям.

    Returns:
        Union[jsonify, tuple]: В случае успеха возвращает JSON с количеством удаленных транзакций.
        В случае ошибки возвращает JSON с описанием ошибки и соответствующим HTTP-кодом.

    Examples:
        >>> DELETE /api/transactions
        >>> {"category": "Food", "date": "2023-01-01", "type": "расход"}
        <<< 200 OK
        <<< {"status": "success", "message": "Deleted 3 transactions", "deleted_count": 3}
    """
    data: Dict[str, Any] = request.get_json()
    
    # Проверяем обязательные поля
    required_fields: List[str] = ['category', 'date', 'type']
    if not all(field in data for field in required_fields):
        return jsonify({
            "status": "error",
            "message": "Missing required fields (category, date, type)"
        }), 400

    try:
        # Ищем и удаляем все подходящие транзакции
        deleted_transactions: int = Transaction.query.filter_by(
            category=data['category'],
            date=data['date'],
            type=data['type']
        ).delete()
        
        db.session.commit()
        
        return jsonify({
            "status": "success",
            "message": f"Deleted {deleted_transactions} transactions",
            "deleted_count": deleted_transactions
        })
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Создаём таблицы в БД, если их нет
    app.run(host="0.0.0.0", port=5000, debug=True)