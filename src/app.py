from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import streamlit as st

from src.database import SessionLocal, init_db
from src.models import Alimento, Fornecedor, Insumo, Pessoa

st.set_page_config(page_title="Festa IFC", layout="wide")
init_db()


def render_home() -> None:
    st.title("Festa IFC - Organização da Feira")
    st.markdown(
        """
        Este sistema ajuda a planejar a festa do IFC Campus Blumenau, registrando os alimentos a serem vendidos,
        os insumos doados, os fornecedores e as pessoas que vão atuar na organização e execução do evento.
        """
    )

    ambiente = os.getenv("APP_ENV", "local").lower()
    st.info(f"Ambiente atual: {ambiente} | Banco: SQLite local, ou MySQL em produção.")

    st.subheader("Resumo do contexto")
    st.write(
        "- Alimentos para venda com preços definidos.\n"
        "- Insumos doados por parceiros e pessoas da comunidade.\n"
        "- Pessoas envolvidas no evento, incluindo alunos, pais de alunos e servidores.\n"
        "- Organização dos registros para facilitar a logística da festa."
    )


def render_fornecedores() -> None:
    st.title("CRUD - Fornecedores")
    key_prefix = "fornecedor"
    selected_id = st.session_state.get(f"{key_prefix}_selected_id")

    with SessionLocal() as session:
        fornecedores = session.query(Fornecedor).order_by(Fornecedor.nome).all()
        if selected_id:
            current = session.query(Fornecedor).filter(Fornecedor.id == selected_id).first()
        else:
            current = None

        st.subheader("Lista de fornecedores")
        if not fornecedores:
            st.warning("Nenhum fornecedor cadastrado.")
        else:
            for fornecedor in fornecedores:
                col_nome, col_editar, col_excluir = st.columns([4, 1, 1])
                with col_nome:
                    st.write(f"{fornecedor.nome} ({fornecedor.tipo})")
                with col_editar:
                    if st.button("Editar", key=f"{key_prefix}_edit_{fornecedor.id}"):
                        st.session_state[f"{key_prefix}_selected_id"] = fornecedor.id
                        st.rerun()
                with col_excluir:
                    if st.button("Excluir", key=f"{key_prefix}_delete_{fornecedor.id}"):
                        session.delete(fornecedor)
                        session.commit()
                        if st.session_state.get(f"{key_prefix}_selected_id") == fornecedor.id:
                            st.session_state[f"{key_prefix}_selected_id"] = None
                        st.rerun()

        st.subheader("Cadastro / Edição")
        with st.form(f"{key_prefix}_form"):
            nome = st.text_input("Nome", value=current.nome if current else "")
            tipo = st.selectbox(
                "Tipo",
                ["Empresa", "Pessoa física", "Organização", "Comunidade"],
                index=["Empresa", "Pessoa física", "Organização", "Comunidade"].index(current.tipo)
                if current else 0,
            )
            contato = st.text_input("Contato", value=current.contato if current else "")
            telefone = st.text_input("Telefone", value=current.telefone if current else "")
            descricao = st.text_area("Descrição", value=current.descricao if current else "")

            submitted = st.form_submit_button("Salvar fornecedor")
            if submitted:
                if current:
                    current.nome = nome
                    current.tipo = tipo
                    current.contato = contato
                    current.telefone = telefone
                    current.descricao = descricao
                    session.commit()
                    st.success("Fornecedor atualizado com sucesso!")
                else:
                    fornecedor = Fornecedor(
                        nome=nome,
                        tipo=tipo,
                        contato=contato,
                        telefone=telefone,
                        descricao=descricao,
                    )
                    session.add(fornecedor)
                    session.commit()
                    st.success("Fornecedor cadastrado com sucesso!")

                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()

        if current:
            if st.button("Cancelar edição"):
                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()


def render_insumos() -> None:
    st.title("CRUD - Insumos")
    key_prefix = "insumo"
    selected_id = st.session_state.get(f"{key_prefix}_selected_id")

    with SessionLocal() as session:
        insumos = session.query(Insumo).order_by(Insumo.nome).all()
        fornecedores = session.query(Fornecedor).order_by(Fornecedor.nome).all()
        current = session.query(Insumo).filter(Insumo.id == selected_id).first() if selected_id else None

        st.subheader("Lista de insumos")
        if not insumos:
            st.warning("Nenhum insumo cadastrado.")
        else:
            for insumo in insumos:
                col_nome, col_editar, col_excluir = st.columns([4, 1, 1])
                with col_nome:
                    fornecedor_nome = insumo.fornecedor.nome if insumo.fornecedor else "Sem fornecedor"
                    st.write(f"{insumo.nome} - {insumo.quantidade} unidades ({fornecedor_nome})")
                with col_editar:
                    if st.button("Editar", key=f"{key_prefix}_edit_{insumo.id}"):
                        st.session_state[f"{key_prefix}_selected_id"] = insumo.id
                        st.rerun()
                with col_excluir:
                    if st.button("Excluir", key=f"{key_prefix}_delete_{insumo.id}"):
                        session.delete(insumo)
                        session.commit()
                        if st.session_state.get(f"{key_prefix}_selected_id") == insumo.id:
                            st.session_state[f"{key_prefix}_selected_id"] = None
                        st.rerun()

        st.subheader("Cadastro / Edição")
        with st.form(f"{key_prefix}_form"):
            nome = st.text_input("Nome do insumo", value=current.nome if current else "")
            quantidade = st.number_input(
                "Quantidade",
                min_value=0,
                step=1,
                value=int(current.quantidade) if current else 0,
            )
            doado = st.checkbox("Foi doado?", value=current.doado if current else True)
            fornecedor_opcoes = ["Nenhum"] + [f.nome for f in fornecedores]
            fornecedor_nome = current.fornecedor.nome if current and current.fornecedor else "Nenhum"
            fornecedor_index = fornecedor_opcoes.index(fornecedor_nome) if fornecedor_nome in fornecedor_opcoes else 0
            fornecedor_selecionado = st.selectbox("Fornecedor", fornecedor_opcoes, index=fornecedor_index)
            observacao = st.text_area("Observação", value=current.observacao if current else "")

            submitted = st.form_submit_button("Salvar insumo")
            if submitted:
                fornecedor = None
                if fornecedor_selecionado != "Nenhum":
                    fornecedor = session.query(Fornecedor).filter(Fornecedor.nome == fornecedor_selecionado).first()

                if current:
                    current.nome = nome
                    current.quantidade = quantidade
                    current.doado = doado
                    current.observacao = observacao
                    current.fornecedor = fornecedor
                    session.commit()
                    st.success("Insumo atualizado com sucesso!")
                else:
                    novo_insumo = Insumo(
                        nome=nome,
                        quantidade=quantidade,
                        doado=doado,
                        observacao=observacao,
                        fornecedor=fornecedor,
                    )
                    session.add(novo_insumo)
                    session.commit()
                    st.success("Insumo cadastrado com sucesso!")

                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()

        if current:
            if st.button("Cancelar edição"):
                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()


def render_pessoas() -> None:
    st.title("CRUD - Pessoas")
    key_prefix = "pessoa"
    selected_id = st.session_state.get(f"{key_prefix}_selected_id")

    with SessionLocal() as session:
        pessoas = session.query(Pessoa).order_by(Pessoa.nome).all()
        current = session.query(Pessoa).filter(Pessoa.id == selected_id).first() if selected_id else None

        st.subheader("Lista de pessoas")
        if not pessoas:
            st.warning("Nenhuma pessoa cadastrada.")
        else:
            for pessoa in pessoas:
                col_nome, col_editar, col_excluir = st.columns([4, 1, 1])
                with col_nome:
                    st.write(f"{pessoa.nome} - {pessoa.tipo} ({pessoa.funcao})")
                with col_editar:
                    if st.button("Editar", key=f"{key_prefix}_edit_{pessoa.id}"):
                        st.session_state[f"{key_prefix}_selected_id"] = pessoa.id
                        st.rerun()
                with col_excluir:
                    if st.button("Excluir", key=f"{key_prefix}_delete_{pessoa.id}"):
                        session.delete(pessoa)
                        session.commit()
                        if st.session_state.get(f"{key_prefix}_selected_id") == pessoa.id:
                            st.session_state[f"{key_prefix}_selected_id"] = None
                        st.rerun()

        st.subheader("Cadastro / Edição")
        with st.form(f"{key_prefix}_form"):
            nome = st.text_input("Nome", value=current.nome if current else "")
            tipo = st.selectbox(
                "Tipo",
                ["Aluno", "Pai de aluno", "Servidor"],
                index=["Aluno", "Pai de aluno", "Servidor"].index(current.tipo)
                if current else 0,
            )
            funcao = st.text_input("Função na festa", value=current.funcao if current else "")
            contato = st.text_input("Contato", value=current.contato if current else "")
            disponibilidade = st.text_input("Disponibilidade", value=current.disponibilidade if current else "")

            submitted = st.form_submit_button("Salvar pessoa")
            if submitted:
                if current:
                    current.nome = nome
                    current.tipo = tipo
                    current.funcao = funcao
                    current.contato = contato
                    current.disponibilidade = disponibilidade
                    session.commit()
                    st.success("Pessoa atualizada com sucesso!")
                else:
                    pessoa = Pessoa(
                        nome=nome,
                        tipo=tipo,
                        funcao=funcao,
                        contato=contato,
                        disponibilidade=disponibilidade,
                    )
                    session.add(pessoa)
                    session.commit()
                    st.success("Pessoa cadastrada com sucesso!")

                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()

        if current:
            if st.button("Cancelar edição"):
                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()


def render_alimentos() -> None:
    st.title("CRUD - Alimentos")
    key_prefix = "alimento"
    selected_id = st.session_state.get(f"{key_prefix}_selected_id")

    with SessionLocal() as session:
        alimentos = session.query(Alimento).order_by(Alimento.nome).all()
        fornecedores = session.query(Fornecedor).order_by(Fornecedor.nome).all()
        current = session.query(Alimento).filter(Alimento.id == selected_id).first() if selected_id else None

        st.subheader("Lista de alimentos")
        if not alimentos:
            st.warning("Nenhum alimento cadastrado.")
        else:
            for alimento in alimentos:
                col_nome, col_editar, col_excluir = st.columns([4, 1, 1])
                with col_nome:
                    fornecedor_nome = alimento.fornecedor.nome if alimento.fornecedor else "Sem fornecedor"
                    st.write(f"{alimento.nome} - R$ {alimento.preco_venda:.2f} ({fornecedor_nome})")
                with col_editar:
                    if st.button("Editar", key=f"{key_prefix}_edit_{alimento.id}"):
                        st.session_state[f"{key_prefix}_selected_id"] = alimento.id
                        st.rerun()
                with col_excluir:
                    if st.button("Excluir", key=f"{key_prefix}_delete_{alimento.id}"):
                        session.delete(alimento)
                        session.commit()
                        if st.session_state.get(f"{key_prefix}_selected_id") == alimento.id:
                            st.session_state[f"{key_prefix}_selected_id"] = None
                        st.rerun()

        st.subheader("Cadastro / Edição")
        with st.form(f"{key_prefix}_form"):
            nome = st.text_input("Nome do alimento", value=current.nome if current else "")
            categoria = st.selectbox(
                "Categoria",
                ["Salgado", "Doce", "Bebida", "Outros"],
                index=["Salgado", "Doce", "Bebida", "Outros"].index(current.categoria)
                if current else 0,
            )
            quantidade = st.number_input(
                "Quantidade disponível",
                min_value=0,
                step=1,
                value=int(current.quantidade_disponivel) if current else 0,
            )
            preco_venda = st.number_input(
                "Preço de venda",
                min_value=0.0,
                step=0.5,
                value=float(current.preco_venda) if current else 0.0,
            )
            fornecedor_opcoes = ["Nenhum"] + [f.nome for f in fornecedores]
            fornecedor_nome = current.fornecedor.nome if current and current.fornecedor else "Nenhum"
            fornecedor_index = fornecedor_opcoes.index(fornecedor_nome) if fornecedor_nome in fornecedor_opcoes else 0
            fornecedor_selecionado = st.selectbox("Fornecedor", fornecedor_opcoes, index=fornecedor_index)
            descricao = st.text_area("Descrição", value=current.descricao if current else "")

            submitted = st.form_submit_button("Salvar alimento")
            if submitted:
                fornecedor = None
                if fornecedor_selecionado != "Nenhum":
                    fornecedor = session.query(Fornecedor).filter(Fornecedor.nome == fornecedor_selecionado).first()

                if current:
                    current.nome = nome
                    current.categoria = categoria
                    current.quantidade_disponivel = quantidade
                    current.preco_venda = preco_venda
                    current.descricao = descricao
                    current.fornecedor = fornecedor
                    session.commit()
                    st.success("Alimento atualizado com sucesso!")
                else:
                    alimento = Alimento(
                        nome=nome,
                        categoria=categoria,
                        quantidade_disponivel=quantidade,
                        preco_venda=preco_venda,
                        descricao=descricao,
                        fornecedor=fornecedor,
                    )
                    session.add(alimento)
                    session.commit()
                    st.success("Alimento cadastrado com sucesso!")

                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()

        if current:
            if st.button("Cancelar edição"):
                st.session_state[f"{key_prefix}_selected_id"] = None
                st.rerun()


def main() -> None:
    st.sidebar.title("Menu")
    page = st.sidebar.radio(
        "Navegação",
        ["Início", "Fornecedores", "Insumos", "Pessoas", "Alimentos"],
    )

    if page == "Início":
        render_home()
    elif page == "Fornecedores":
        render_fornecedores()
    elif page == "Insumos":
        render_insumos()
    elif page == "Pessoas":
        render_pessoas()
    else:
        render_alimentos()


if __name__ == "__main__":
    main()
