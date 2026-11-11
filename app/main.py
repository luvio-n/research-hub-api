# Depends позволяет FastAPI получить сессию базы данных через get_db()
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Material
from app.schemas.material import MaterialResponse, MaterialCreate, MaterialUpdate

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Research Hub API is running"}

@app.get("/materials", response_model=list[MaterialResponse])
# FastAPI вызывает get_db() и передает полученную сессию в параметр db
def get_materials(db: Session = Depends(get_db)):
    materials = db.query(Material).all()

    return materials

@app.post("/materials", response_model=MaterialResponse, status_code=201)
def create_material(
    material_data: MaterialCreate, 
    db: Session = Depends(get_db)):
    new_material = Material(**material_data.model_dump())

    db.add(new_material)
    db.commit()
    db.refresh(new_material)

    return new_material

@app.get("/materials/{material_id}", response_model=MaterialResponse)
def get_material(material_id: int, db: Session = Depends(get_db)):
    material = db.query(Material).filter(Material.id == material_id).first()

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found",
        )

    return material

@app.get("/search")
def search_materials(query: str, db: Session = Depends(get_db)):
    materials = db.query(Material).filter(
        Material.title.ilike(f"%{query}%")
    ).all()
    return materials


@app.get("/db-check")
def check_database(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    return {"database_connected": result.scalar() == 1}

@app.put("/materials/{material_id}", response_model=MaterialResponse)
def update_material(
    material_id: int,
    material_data: MaterialUpdate,
    db: Session = Depends(get_db)
):
    material = db.query(Material).filter(
        Material.id == material_id
    ).first()

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found",
        )

    update_data = material_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(material, field, value)

    db.commit()
    db.refresh(material)

    return material

@app.delete("/materials/{material_id}", status_code=204)
def delete_material(
    material_id: int,
    db: Session = Depends(get_db)
):
    material = db.query(Material).filter(
        Material.id == material_id
    ).first()

    if material is None:
        raise HTTPException(
            status_code=404,
            detail="Material not found",
        )

    db.delete(material)
    db.commit()