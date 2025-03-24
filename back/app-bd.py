from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app = Flask(__name__)
CORS(app)  # Permite requisições do frontend

# Configuração do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Welcome@ads'
app.config['MYSQL_DB'] = 'cad_cli'
app.config['JWT_SECRET_KEY'] = 'chave_secreta'

mysql = MySQL(app)
jwt = JWTManager(app)

# Rota para obter usuários
@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nome, endereco, cidade, email, fone FROM usuarios")
    users = cur.fetchall()
    cur.close()
    
    return jsonify([{"id": u[0], "nome": u[1], "endereco": u[2], "cidade": u[3], "email": u[4], "fone": u[5],} for u in users])

# Rota para cadastro de usuários
@app.route('/registro', methods=['POST'])
def register():
    data = request.get_json()
    nome = data['nome']
    endereco = data['endereco']
    cidade = data['cidade']
    email = data['email']
    fone = data['fone']
    #senha = bcrypt.hashpw(data['senha'].encode('utf-8'), bcrypt.gensalt())

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO cliente (nome, endereco, cidade, fone, email) VALUES (%s, %s, %s, %s, %s)", (nome, endereco, cidade, email, fone))
    mysql.connection.commit()
    cur.close()

    return jsonify({"mensagem": "Usuário registrado com sucesso!"})

# Rota de login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    senha = data['senha'].encode('utf-8')

    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nome, senha FROM usuarios WHERE email = %s", (email,))
    user = cur.fetchone()
    cur.close()

    if user and bcrypt.checkpw(senha, user[2].encode('utf-8')):
        token = create_access_token(identity={"id": user[0], "nome": user[1]})
        return jsonify({"token": token})
    return jsonify({"erro": "Credenciais inválidas"}), 401

# Rota protegida para testar autenticação
@app.route('/perfil', methods=['GET'])
@jwt_required()
def perfil():
    usuario = get_jwt_identity()
    return jsonify({"mensagem": f"Bem-vindo, {usuario['nome']}!"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)