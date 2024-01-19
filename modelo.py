import datetime
from app import db


#Modelos
class usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    telefono = db.Column(db.String(20))

    # Relacion uno a muchos
    ingresos = db.relationship("ingresos", back_populates="usuario")
    gastos = db.relationship("gastos", back_populates="usuario")

    def __str__(self):
        return (
            f"Id:{self.id}"
            f"telefono:{self.telefono}"
        )
        
class ingreso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto_ingreso = db.Column(db.String(20))
    fecha = db.Column(db.DateTime,  default=datetime)
    nota = db.Column(db.String(255))
    
    # Relacion con la tabla usuario
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    usuario = db.relationship("usuario", back_populates="ingresos")


    def __str__(self):
        return(
            f"id:{self.id}"
            f"monto_ingreso:{self.monto_ingreso}"
            f"fecha: {self.fecha}"
        )

class gasto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto_gasto = db.Column(db.String(20))
    fecha = db.Column(db.DateTime, default=datetime)
    nota = db.Column(db.String(255))
    
    # Relacion con la tabla usuario
    id_usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    usuario = db.relationship("usuario", back_populates="gasto")


    def __str__(self):
        return(
            f"id:{self.id}"
            f"monto_gasto:{self.monto_ingreso}"
            f"fecha: {self.fecha}"
        )