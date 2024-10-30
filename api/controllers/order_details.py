from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import models, schemas


def create(db: Session, orderr):
    # Create a new instance of the OrderDetail model with the provided data
    db_orderDetail = models.OrderDetail(
        order_id=orderr.order_id,
        sandwich_id=orderr.sandwich_id,
        amount=orderr.amount
    )
    # Add the newly created OrderDetail object to the database session
    db.add(db_orderDetail)
    # Commit the changes to the database
    db.commit()
    # Refresh the OrderDetail object to ensure it reflects the current state in the database
    db.refresh(db_orderDetail)
    # Return the newly created OrderDetail object
    return db_orderDetail


def read_all(db: Session):
    return db.query(models.OrderDetail).all()


def read_one(db: Session, order_id):
    return db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id).first()


def update(db: Session, order_id, order):
    # Query the database for the specific orderDetail to update
    db_order = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id)
    # Extract the update data from the provided 'orderDetail' object
    update_data = order.model_dump(exclude_unset=True)
    # Update the database record with the new data, without synchronizing the session
    db_order.update(update_data, synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return the updated orderDetail record
    return db_order.first()


def delete(db: Session, order_id):
    # Query the database for the specific orderDetail to delete
    db_order = db.query(models.OrderDetail).filter(models.OrderDetail.id == order_id)
    # Delete the database record without synchronizing the session
    db_order.delete(synchronize_session=False)
    # Commit the changes to the database
    db.commit()
    # Return a response with a status code indicating success (204 No Content)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
