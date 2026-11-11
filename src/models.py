from __future__ import annotations

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from src.database import Base


class Fornecedor(Base):
    __tablename__ = "fornecedores"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    tipo = Column(String(80), nullable=False)
    contato = Column(String(150), nullable=False)
    telefone = Column(String(50), nullable=True)
    descricao = Column(String(255), nullable=True)

    insumos = relationship("Insumo", back_populates="fornecedor")
    alimentos = relationship("Alimento", back_populates="fornecedor")


class Insumo(Base):
    __tablename__ = "insumos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    quantidade = Column(Integer, nullable=False, default=0)
    doado = Column(Boolean, nullable=False, default=True)
    observacao = Column(String(255), nullable=True)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)

    fornecedor = relationship("Fornecedor", back_populates="insumos")


class Pessoa(Base):
    __tablename__ = "pessoas"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    tipo = Column(String(40), nullable=False)
    funcao = Column(String(120), nullable=False)
    contato = Column(String(150), nullable=True)
    disponibilidade = Column(String(120), nullable=True)


class Alimento(Base):
    __tablename__ = "alimentos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(120), nullable=False)
    categoria = Column(String(60), nullable=False)
    quantidade_disponivel = Column(Integer, nullable=False, default=0)
    preco_venda = Column(Float, nullable=False, default=0.0)
    descricao = Column(String(255), nullable=True)
    fornecedor_id = Column(Integer, ForeignKey("fornecedores.id"), nullable=True)

    fornecedor = relationship("Fornecedor", back_populates="alimentos")
