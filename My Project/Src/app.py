from flask import Flask, render_template, request, redirect, session
from models.IDatabase import IDatabase

# Create Init App
app = Flask(__name__)
app.secret_key = "I4104@Key_of_app"

conn = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "final"
}

IDatabase = IDatabase(conn, debug = True)

@app.route("/", methods=['GET'])
def index():
    if 'username' not in session:
        return redirect("/login")
    data = IDatabase.get("books")
    return render_template('index.html', data = data)

@app.route("/search", methods=['GET'])
def search():
    if 'username' not in session:
        return redirect("/login")
    search = request.args.get('search')
    data = IDatabase.get("books", [
        f"title LIKE '%{search}%'"
    ])
    return render_template('index.html', data = data, search = search)

@app.route("/rent", methods=['GET', "POST"])
def rent():
    if 'username' not in session:
        return redirect("/login")

    if (request.method == "GET"):
        data = IDatabase.get("rent_books")
        return render_template('rent.html', data = data)

    if (request.method == "POST"):
        id_book = request.form.get("id_book")
        name = request.form.get("name")
        studentId = request.form.get("studentId")

        try:
            IDatabase.insert("rent_books", [
                f"id_book = '{id_book}'",
                f"name = '{name}'",
                f"studentId = '{studentId}'",
            ])
            return {"title": "Thành công", "message": "Cho mượn sách thành công", "type": "success", "reload": True}
        except:
            return {"title": "Thất bại", "message": "Mã sách không tồn tại", "type": "error", "reload": False}



@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect("/")

    if (request.method == "GET"):
        return render_template('login.html')

    if (request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")

        users = IDatabase.get("users", [
            f"username = '{username}'",
            f"password = '{password}'"
        ])

        if users:
            session["username"] = username
            return {"title": "Thành công", "message": "Đăng nhập thành công", "type": "success", "reload": True}
        else:
            return {"title": "Thất bại", "message": "Tài khoản mật khẩu không chính xác", "type": "error", "reload": False}

@app.route("/register", methods=['GET', 'POST'])
def register():
    if 'username' in session:
        return redirect("/")

    if (request.method == "GET"):
        return render_template('register.html')

    if (request.method == "POST"):
        username = request.form.get("username")
        password = request.form.get("password")

        users = IDatabase.get("users", [
            f"username = '{username}'"
        ])

        if users:
            return {"title": "Thất bại", "message": "Tài khoản đã tồn tại", "type": "error", "reload": False}
        else:
            IDatabase.insert("users", [
                f"username = '{username}'",
                f"password = '{password}'",
            ])
            session["username"] = username
            return {"title": "Thành công", "message": "Đăng ký thành công", "type": "success", "reload": True}

@app.route("/add", methods=['GET', 'POST'])
def add():
    if 'username' not in session:
        return redirect("/login")

    if (request.method == "GET"):
        return render_template('add.html')

    if (request.method == "POST"):
        name = request.form.get('name')
        author = request.form.get('author')
        tags = request.form.get('tags')
        year_xb = request.form.get('year_xb')

        if (name == "" or author == "" or tags  == "" or year_xb == ""):
            return {"title": "Thất bại", "message": f"Vui lòng nhập đủ thông tin: {name}", "type": "error", "reload": False}
        else:
            IDatabase.insert("books", [
                f"title = '{name}'",
                f"author = '{author}'",
                f"tags = '{tags}'",
                f"year_xb = '{year_xb}'",
            ])
        return {"title": "Thành công", "message": "Thêm sách mới thành công", "type": "success", "reload": True}

@app.route("/edit/<id>", methods=['GET', 'POST'])
def edit(id):
    if 'username' not in session:
        return redirect("/login")
    data = IDatabase.get("books", [f"id = {id}"])

    if (request.method == "GET"):
        if data:
            # Lấy dòng dữ liệu đầu tiên của table book
            return render_template('edit.html', data = data[0])
        return "<script>alert('Sách của bạn không tồn tại!'); window.history.go(-1); </script>";

    if (request.method == "POST"):
        if data:
            name = request.form.get('name')
            author = request.form.get('author')
            tags = request.form.get('tags')
            year_xb = request.form.get('year_xb')

            if (name == "" or author == "" or tags  == "" or year_xb == ""):
                return {"title": "Thất bại", "message": "Vui lòng nhập đủ thông tin", "type": "error", "reload": False}
            else:
                IDatabase.update("books", [
                    f"title = '{name}'",
                    f"author = '{author}'",
                    f"tags = '{tags}'",
                    f"year_xb = '{year_xb}'",
                ], [ f"id = {id}" ])        
            return { "title": "Thành công", "message": "Đã lưu thay đổi", "type": "success", "reload": True }
        return { "title": "Thất bại", "message": "Sách này không tồn tại!", "type": "error", "reload": True }

@app.route("/delete/<id>", methods=['GET'])
def delete(id):
    data = IDatabase.get("book", [f"id = {id}"]);
    if data:
        IDatabase.delete("book", [f"id = {id}"])
        return { "title": "Thành công", "message": "Đã xoá sách thành công", "type": "success", "reload": True }
    
    return { "title": "Thất bại", "message": "Sách này không tồn tại!", "type": "error", "reload": True }

app.run(debug=True)
