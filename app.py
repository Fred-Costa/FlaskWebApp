from flask import Flask, render_template, request, redirect, url_for
from connection.conexaoDB import conn

app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')


@app.route('/index')
def listar_produtos():
    cursor = conn.cursor()

    sql = """
            SELECT p.nome, p.preco, c.nome
            FROM produtos p
            JOIN categorias c 
            ON p.id_categoria = c.id
          """
    cursor.execute(sql)

    produtos = cursor.fetchall()

    return render_template('index.html', produtos=produtos)


@app.route('/login', methods=['GET', 'POST'])
def checkUser():
    if request.method == "POST":
        # Guarda os inputs do utilizador em variaveis
        user = request.form['user']
        password = request.form['password']

        # objeto para interagir com a base de dados
        cursor = conn.cursor()

        # query de SQL para verificar se as credenciais que o user colocou sao iguais as que tem na base de dados
        sql = "SELECT user, password FROM credenciais WHERE user = %s AND password = %s"

        cursor.execute(sql, (user, password))

        # recupera os valores e guarda-os na variável
        dados_user = cursor.fetchone()

        if dados_user is not None and dados_user[0] == user and dados_user[1] == password:
            # se os inputs do utilizador forem corretos, o login foi bem sucedido
            return redirect(url_for('listar_produtos'))
        else:
            return render_template('erro.html')


def checkCredenciais(email, user):
    cursor = conn.cursor()

    sql = "SELECT email, user FROM credenciais WHERE email = %s OR user = %s"
    cursor.execute(sql, (email, user))

    dados = cursor.fetchone()
    cursor.close()

    if dados is not None:
        # credenciais já existem
        return True
    else:
        # credenciais não existem
        return False


@app.route('/registoLogin')
def registo_login():
    return render_template('registoLogin.html')


@app.route('/registoLogin', methods=['GET', 'POST'])
def registo():
    if request.method == 'POST':
        # guarda os inputs do formulario e guarda em variáveis
        nome = request.form['nome']
        email = request.form['email']
        user = request.form['user']
        password = request.form['password']

        if checkCredenciais(email, user):
            return render_template('erro.html')
        else:
            # abrir o cursor para interagir com a base de dados
            cursor = conn.cursor()

            # string sql guardar valores nos campos especificos
            sql = "INSERT INTO credenciais (nome, email, user, password) VALUES (%s, %s, %s, %s)"

            # executar e guardar a string sql com os valores passados
            cursor.execute(sql, (nome, email, user, password))
            conn.commit()

            # fechar o cursor
            cursor.close()

            return redirect(url_for('login'))


@app.route('/registoProduto', methods=['GET', 'POST'])
def registoProduto():
    with conn.cursor() as cursor:
        sqlCategoria = 'SELECT * FROM categorias'
        cursor.execute(sqlCategoria)
        categorias = cursor.fetchall()

        if request.method == 'POST':
            # guardar os inputs do formulario em variaveis
            nomeProduto = request.form['nomeProduto']
            preco = request.form['preco']
            categoriaID = request.form['categoria']

            sql = 'INSERT INTO produtos (nome, preco, id_categoria) VALUES (%s, %s, %s)'
            try:
                cursor.execute(sql, (nomeProduto, preco, categoriaID))
                conn.commit()
            except Exception as erro:
                conn.rollback()
                print(f'Erro em registar o novo produto: {erro}')

            return redirect(url_for('listar_produtos'))

        return render_template('createProduto.html', categorias=categorias)


@app.route('/deleteProduto', methods=['GET', 'POST'])
def deleteProduto():
    # Se o request for apenas de GET - mostra os produtos
    with conn.cursor() as cursor:
        sqlProdutos = "SELECT * FROM produtos"
        cursor.execute(sqlProdutos)
        produtos = cursor.fetchall()

        if request.method == 'POST':
            idProduto = request.form['produto']

            sql = 'DELETE FROM produtos WHERE id = (%s)'
            try:
                cursor.execute(sql, (idProduto,))
                conn.commit()
            except Exception as erro:
                conn.rollback()
                print(f"Erro em apagar o produto: {erro}")

            return redirect(url_for('listar_produtos'))

    return render_template('deleteProduto.html', produtos=produtos)


if __name__ == "__main__":
    app.run(debug=True)
