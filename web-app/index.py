"""

Flask to Perform Actions on WebApp
@author: Sainath Sapa, 7518
@for : Tiger Analytics India Consulting Private Limited
@mentor: Sandeep Arora

"""
# Imports from Python LIB


# from index import app

from flask_mongoengine import MongoEngine
from bson.objectid import ObjectId
from datetime import datetime
import random
import os
from werkzeug.utils import secure_filename
from flask import request, session, redirect, url_for
from flask import Flask, jsonify, render_template
GET_POST = ['GET', 'POST']


# Folder Initialing for File Storage

UPLOAD_FOLDER = 'static/product_images/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check the FileFormat


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# APP_CONFIG for MANGO
app = Flask(__name__)
app.secret_key = 'TigerAnalyticsIndiaConsultingPrivateLimited'
app.config['MONGODB_SETTINGS'] = {
    'db': 'tig',
    'host': 'MongoDB',
    'port': 27017
}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Calling and Initialing MongoEngine
db = MongoEngine()
db.init_app(app)

"""
Classs Models that we can perform Actions and Store in MongoDB

"""
# Admin Model


class Admin(db.Document):
    _id = db.StringField()
    userName = db.StringField()
    pwd = db.StringField()

    def delete(self, _id):
        adminList = []
        adminList = list(filter(lambda x: x['_id'] != _id, adminList))
        return adminList + " deleted"

    def to_json(self):
        return {"_id": self._id,
                "email": self.userName,
                "pwd": self.pwd}

# USER DETAILS


class User(db.Document):
    _id = db.StringField()
    name = db.StringField()
    email = db.StringField()
    pwd = db.StringField()

    def delete(self, _id):
        userList = []
        userList = list(filter(lambda x: x['_id'] != _id, userList))
        return userList + "deleted"

    def to_json(self):
        return {"_id": self._id,
                "name": self.name,
                "email": self.email,
                "pwd": self.pwd}

# ORDER DETAILS


class Orders(db.Document):
    _id = db.StringField()
    userID = db.StringField()
    itemImage = db.ListField()
    itemName = db.ListField()
    itemDesc = db.ListField()
    itemPrice = db.ListField()
    itemQty = db.ListField()
    orderStatus = db.StringField()
    orderDate = db.StringField()

    def delete(self, _id):
        orderList = []
        orderList = list(filter(lambda x: x['_id'] != _id, orderList))
        return orderList + "deleted"

    def to_json(self):
        return {"_id": self._id,
                "userID": self.userID,
                "itemImage": self.itemImage,
                "itemName": self.itemName,
                "itemDesc": self.itemDesc,
                "itemQty": self.itemQty,
                "orderStatus": self.orderStatus,
                "orderDate": self.orderDate
                }
# Category DETAILS


class Category(db.Document):
    _id = db.StringField()
    catName = db.StringField()
    catDesc = db.StringField()

    def to_json(self):
        return {"_id": self._id,
                "catName": self.catName,
                "catDesc": self.catName
                }

# Item / Product Details


class Items(db.Document):
    _id = db.StringField()
    itemCat = db.StringField()
    itemName = db.StringField()
    itemDesc = db.StringField()
    itemImage = db.StringField()
    itemStock = db.IntField()
    itemPrice = db.StringField()

    def to_json(self):
        return {"_id": self._id,
                "itemCat": self.itemCat,
                "itemName": self.itemName,
                "itemDesc": self.itemDesc,
                'itemImage': self.itemImage,
                "itemStock": self.itemStock,
                "itemPrice": self.itemPrice
                }

# Index Page for Landing


@ app.route('/', methods=['GET'])
def index():
    if not session.get("user_nm") is None:
        return render_template("pages/index.html", show='true'), 200
    else:

        return render_template("pages/index.html", show='false'), 200


@ app.route('/AddAdmin/', methods=['GET'])
def AddAdmin():
    datastr = request.values
    # data=json.loads(datastr)
    name = datastr.get('name')
    pwd = datastr.get('pwd')

    AdminAdd = Admin(userName=name, pwd=pwd).save()
    print(AdminAdd)
    return 'Added', 200


@ app.route('/adminLogin/', methods=GET_POST)
def adminLogin():
    if request.method == 'POST':
        request_string = request.values
        userName = request_string.get('userName')
        pwd = request_string.get('pwd')
        cnt = Admin.objects(userName=userName).count()

        if cnt < 1:
            template = 'admin_pages/login_admin.html'
            return render_template(template, value="noUser"), 200
        else:
            AdminDetails = Admin.objects(
                pwd=pwd, userName=userName).count()

            if AdminDetails >= 1:
                session['userName'] = userName

                userVar = Admin.objects(userName=userName).first()
                session['userName'] = userVar['userName']
                return redirect(url_for('adminPage')), 200
            else:
                template = 'admin_pages/login_admin.html'
                return render_template(template, value="pwd"), 200

    else:

        if session.get('userName'):

            return redirect(url_for('adminPage/')), 200
        else:

            return render_template('admin_pages/login_admin.html'), 200

# This method for Showing Sign Up / Registration Page


@ app.route('/signup/', methods=GET_POST)
def signup():
    if request.method == 'POST':

        # retails_usrs=db.ret_users
        request_string = request.values

        email = request_string.get('email')

        cnt = User.objects(email=email).count()
        if cnt > 1:
            return render_template('/pages/signup.html', value="exits"), 400
        else:

            firstName = request_string.get('fname')
            lastName = request_string.get('lname')
            email = request_string.get('email')
            pwd = request_string.get('pwd')
            name = firstName + " "+lastName

            newUserAdd = User(
                email=email, name=name, pwd=pwd).save()

            session["email"] = email
            session["user_nm"] = firstName + " "+lastName
            print(newUserAdd)
            return redirect(url_for('products/')), 200

    else:
        return render_template('pages/signup.html'), 200

# Show Login Page


@ app.route('/login/', methods=GET_POST)
def login():

    if request.method == 'POST':
        # return "Posted"
        request_string = request.values
        email = request_string.get('email')
        pwd = request_string.get('pwd')
        cnt = User.objects(email=email).count()
        print(cnt)
    #   return " "+str(cnt)
        if cnt < 1:
            return render_template('/pages/login.html', value="noUser"), 400
        else:
            userDetails = User.objects(pwd=pwd, email=email).count()
            # for record in userDetails:
            #      print(record)
            if userDetails >= 1:
                session['email'] = email

                userVar = User.objects(email=email).first()
                session['user_nm'] = userVar['name']
                return redirect(url_for('products')), 200
            else:
                return render_template('/pages/login.html', value="pwd"), 400

    else:

        if session.get('email'):

            return redirect(url_for('products')), 200
        else:
            return render_template('pages/login.html'), 200

# Method for LogOut


@ app.route('/logout/', methods=GET_POST)
def logout():
    session.clear()
    return redirect(url_for('login/')), 200

# Default Login Redirect for User in Products


@ app.route('/products/', methods=GET_POST)
def products():
    if 'user_nm' not in session:
        return redirect(url_for('login')), 400
    else:
        request_string = request.values
        list_cat = Category.objects.all()
        # listItems = Items.objects.all()
        cart_update = ''
        if request_string.get('cart_update'):
            cart_update = request_string.get('cart_update')
            if 'added' in cart_update:
                cart_update = 'added'
        poroduct_list = []
        cat_list = []
        for i in list_cat:
            objInstance = ObjectId(i['_id'])

            poroduct_list.append(Items.objects(itemCat=str(objInstance)))
            cat_list.append(str(ObjectId(i['_id'])))
        template = 'user_pages/products.html'
        usrname = session['user_nm']
        nl = len(list_cat)
        np = len(poroduct_list)
        return render_template(template, Products=poroduct_list,
                               listCat=list_cat, catList=cat_list,
                               value=usrname, nl=nl, np=np,
                               cart_update=cart_update), 200


@ app.route('/itemView/', methods=['GET'])
def itemView():
    if 'user_nm' not in session:
        return redirect(url_for('login/'))
    else:
        request_string = request.values
        cart_update = ""
        id = request_string.get('id')
        objInstance = ObjectId(id)
        listCat = Category.objects.all()
        itemObj = Items.objects(_id=objInstance).first()

        if request_string.get('cart'):
            cart_update = request_string.get('cart')
            if 'added' in cart_update:
                cart_update = 'added'

        return render_template('user_pages/itemView.html', listCat=listCat,
                               itemObj=itemObj,
                               value=session['user_nm'],
                               cart_update=cart_update), 200

# Admin Method Index


@ app.route('/admin/')
def adminPage():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/')), 400
    else:
        return render_template('admin_pages/index.html'), 200

# Add New Category [Admin Method]


@ app.route('/add_cat/', methods=['GET', 'POST'])
def addCat():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:

        listCat = Category.objects.all()
        if request.method == 'POST':
            # return "POST"
            catName = request.form['catNM']
            catDesc = request.form['catDesc']
            newCatAdd = Category(catName=catName, catDesc=catDesc).save()
            print(newCatAdd)
            listCat = Category.objects.all()
        #   print(listCat[0]['_id'])
            return render_template('admin_pages/addCat.html',
                                   value="added",
                                   len=len(listCat),
                                   listCat=listCat
                                   )
        #  print(str(listCat[0]['_id']))

        return render_template("admin_pages/addCat.html",
                               len=len(listCat),
                               listCat=listCat)

# Edit a category [Admin Method]


@ app.route('/editCat/', methods=['GET', 'POST'])
def editCat():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:

        if request.method == 'GET':
            id = request.args.get('id')
            objInstance = ObjectId(id)
            Cat = Category.objects(_id=objInstance).first()
            return render_template('admin_pages/updateCat.html', cat=Cat)

        if request.method == 'POST':
            id = request.form['id']
            objInstance = ObjectId(id)
            Cat = Category.objects(_id=objInstance)
            if not Cat:
                return jsonify({'error': 'data not found'})
            else:
                Cat.update(
                    catName=request.form['catNM'],
                    catDesc=request.form['catDesc'])
                listCat = Category.objects.all()
                return render_template("admin_pages/addCat.html",
                                       len=len(listCat),
                                       listCat=listCat,
                                       value="updated")

# Delete a Category [Admin Method]


@ app.route('/deleteCat/', methods=['GET'])
def deleteCat():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:

        id = request.args.get('id')
        objInstance = ObjectId(id)

        Cat = Category.objects(_id=objInstance)
        if not Cat:
            return jsonify({'error': 'data not found'})
        else:
            Cat.delete()
            listCat = Category.objects.all()

            return render_template("admin_pages/addCat.html",
                                   len=len(listCat),
                                   listCat=listCat,
                                   value="deleted")

# View Category [Admin Method]


@ app.route('/viewCat/', methods=['GET'])
def viewCat():

    id = request.args.get('id')
    objInstance = ObjectId(id)
    catNAME = Category.objects(_id=objInstance).first()
    listCat = Category.objects.all()

    items = Items.objects(itemCat=id)
    if not items:
        return jsonify({'error': 'data not found'})
    else:

        return render_template("user_pages/viewCat.html",
                               len=len(items),
                               items=items,
                               value=session['user_nm'],
                               catNAME=catNAME,
                               listCat=listCat)

# Add New Product [Admin Method]


@app.route('/newProduct/', methods=['GET', 'POST'])
def addNewProduct():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:
        listCat = Category.objects.all()
        print(listCat)
        if request.method == 'POST':
            form = request.form
            itemCat = form['prodCatID']
            itemName = form['prodNM']
            itemDesc = form['prodDesc']
            itemStock = form['prodQTY']
            imageFile = request.files['prodImage']
            itemPrice = form['prodPrice']

            if imageFile and allowed_file(imageFile.filename):
                filename = secure_filename(imageFile.filename)
                filename = str(random.random())+filename
                imageFile.save(os.path.join(UPLOAD_FOLDER, filename))
                newProductAdd = Items(itemCat=itemCat,
                                      itemName=itemName,
                                      itemDesc=itemDesc,
                                      itemImage=str(
                                          os.path.join('/product_images/',
                                                       filename)
                                      ),
                                      itemStock=itemStock,
                                      itemPrice=itemPrice).save()
                print(newProductAdd)

                return render_template('admin_pages/addNewProd.html',
                                       value="added",
                                       listCat=listCat)
                # return jsonify(filename)

        return render_template("admin_pages/addNewProd.html",
                               listCat=listCat)

# View List of Products [Admin Method]


@app.route('/listProduct/', methods=['GET', 'POST'])
def listProduct():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:

        listCat = Category.objects.all()
        # listItems = Items.objects.all()
        productArr = []
        # finalArr = []

        for i in listCat:
            objInstance = ObjectId(i['_id'])

            productArr.append(Items.objects(itemCat=str(objInstance)))
            # productArr.append(Items.objects(itemCat=str(i['_id'])))
            # productArr.append(str(i["_id"]))
        # a=0
        # for i in productArr:
        #     finalArr.append(i[a]['itemCat']==productArr[a]['itemCat'])
        #     a+=1

        return render_template('admin_pages/listProd.html',
                               Product=productArr)

# Edit a product [Admin Method]


@ app.route('/editProduct/', methods=['GET', 'POST'])
def editProduct():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:

        if request.method == 'GET':
            id = request.args.get('id')
            listCat = Category.objects.all()
            objInstance = ObjectId(id)
            Product = Items.objects(_id=objInstance).first()
            update = request.args.get('updated')
            return render_template('admin_pages/editProduct.html',
                                   Product=Product,
                                   listCat=listCat,
                                   update=update)

        if request.method == 'POST':
            id = request.form['id']
            objInstance = ObjectId(id)
            listCat = Category.objects.all()

            form = request.form
            itemCat = form['prodCatID']
            itemName = form['prodNM']
            itemDesc = form['prodDesc']
            itemStock = form['prodQTY']
            Product = Items.objects(_id=objInstance)
            if not Product:
                return jsonify({'error': 'data not found'})
            else:
                Product.update(itemCat=itemCat,
                               itemName=itemName,
                               itemDesc=itemDesc,
                               itemStock=itemStock)
                return redirect(
                    url_for('editProduct',
                            id=id,
                            updated='true')
                )

# Delete a product [Admin Method]


@ app.route('/deleteProduct/', methods=['GET'])
def deleteProduct():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:
        id = request.args.get('id')
        objInstance = ObjectId(id)

        Item = Items.objects(_id=objInstance)
        if not Item:
            return jsonify({'error': 'data not found'})
        else:
            Item.delete()

            return redirect(url_for('listProduct'))

# View List of Orders [Admin Method]


@ app.route('/listOrders/', methods=['GET'])
def listOrders():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:
        id = request.args.get('id')
        update = request.args.get('updated')
        deleted = request.args.get('deleted')

        listOrders = Orders.objects.all()
        return render_template('admin_pages/listOrders.html',
                               listOrders=listOrders,
                               id=id,
                               update=update,
                               deleted=deleted)

# Update Order [Admin Method]


@ app.route('/updateOrder/', methods=['GET', 'POST'])
def updateOrder():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:

        if request.method == 'GET':
            id = request.args.get('id')

            objInstance = ObjectId(id)
            Order = Orders.objects(_id=objInstance).first()
            # update = request.args.get('updated')
            orderPrice = 0

            cnt = 0
            for i in Order.itemPrice:
                orderPrice += int(i)*int(Order.itemQty[cnt])
                cnt += 1
            orderQty = 0

            for i in Order.itemQty:
                orderQty += int(i)
            return render_template('admin_pages/updateOrder.html',
                                   order=Order,
                                   length=len(Order.itemImage),
                                   orderPrice=orderPrice,
                                   orderQty=orderQty)

        if request.method == 'POST':
            id = request.form['id']
            objInstance = ObjectId(id)

            form = request.form
            status = form.get('status')
            Order = Orders.objects(_id=objInstance)
            if not Order:
                return jsonify({'error': 'data not found'})
            else:

                Order.update(orderStatus=status)
                return redirect(url_for('listOrders',
                                        id=id,
                                        updated='true'))

# Delete Order [Admin Method]


@ app.route('/deleteOrder/', methods=['GET'])
def deleteOrder():
    if not session.get("userName"):
        return redirect(url_for('adminLogin/'))
    else:
        id = request.args.get('id')
        objInstance = ObjectId(id)

        order = Orders.objects(_id=objInstance)
        if not order:
            return jsonify({'error': 'data not found'})
        else:
            order.delete()

            return redirect(url_for('listOrders/', id=id, deleted='true'))

# Method for Init Add to Product to Cart [User Method]


@ app.route('/addCart/', methods=['GET'])
def addCart():
    if 'user_nm' not in session:
        return redirect(url_for('login'))
    else:
        id = request.args.get('id')
        # objInstance = ObjectId(id)
        if 'cartItems' not in session:
            session['cartItems'] = []  #

        cart_list = session['cartItems']
        if id not in cart_list:
            cart_list.append(id)

        session['cartItems'] = cart_list  #

        return redirect(url_for('products/', cart_update='added'))

# User View Cart [User Method]


@ app.route('/viewCart/', methods=['GET'])
def viewCart():
    if 'user_nm' not in session:
        return redirect(url_for('login'))
    else:
        listCat = Category.objects.all()

        if 'cartItems' not in session:

            return "No Items in Cart"
        elif len(session['cartItems']) <= 0:
            return "No Items in Cart"
        else:
            cart_list = session['cartItems']

            itemArr = []
            # return jsonify(cart_list)
            for i in cart_list:
                obj = ObjectId(i)
                tempItem = Items.objects.filter(_id=obj)
                itemArr.append(tempItem)
            # return jsonify(itemArr)

            return render_template('user_pages/viewCart.html',
                                   itemArr=itemArr,
                                   value=session['user_nm'],
                                   listCat=listCat)

# Method for Place Order [User Method]


@ app.route('/placeOrder/', methods=['POST'])
def placeOrder():
    if 'user_nm' not in session:
        return redirect(url_for('login/'))
    else:
        form = request.form
        # finalMap = []
        id = form.getlist('itemId')
        img = form.getlist('img')
        names = form.getlist('name')
        desc = form.getlist('desc')
        price = form.getlist('price')
        qty = form.getlist('qty')
        userEmail = session['email']
        saveOrder = 1
        datetimenow = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        saveOrder = Orders(userID=userEmail,
                           itemImage=img,
                           itemName=names,
                           itemDesc=desc,
                           itemPrice=price,
                           itemQty=qty,
                           orderStatus="Ordered",
                           orderDate=str(datetimenow).save()
                           )
        if(saveOrder):
            cart_list = session['cartItems']
            cart_list.clear()
            session['cartItems'] = cart_list
            for i in range(0, len(id)):
                objInstance = ObjectId(id[i])
                tempItem = Items.objects(_id=objInstance)
                tempStock = int(tempItem[0]['itemStock']) - int(qty[i])
                tempItem.update(itemStock=tempStock)

            # myLastOrder = Orders.objects(userID=userEmail).first()
            return redirect(url_for('user_orders/'))
        else:
            return "error"

# List User Orders [User Method]


@ app.route('/user_orders/', methods=['GET'])
def user_orders():
    listCat = Category.objects.all()

    getOrder = Orders.objects(userID=session['email'])

    return render_template('user_pages/userOrders.html',
                           orders=getOrder,
                           value=session['user_nm'],
                           listCat=listCat)

# View Order [User Method]


@ app.route('/viewOrder/', methods=['GET'])
def viewOrder():
    getID = request.args.get('id')
    objInstance = ObjectId(getID)

    getOrder = Orders.objects(_id=objInstance).first()

    # return jsonify(len(getOrder.itemImage))
    orderPrice = 0
    cnt = 0
    for i in getOrder.itemPrice:
        orderPrice += int(i)*int(getOrder.itemQty[cnt])
        cnt += 1

    orderQty = 0

    for i in getOrder.itemQty:
        orderQty += int(i)

    return render_template('user_pages/viewOrder.html',
                           value=session['user_nm'],
                           order=getOrder,
                           length=len(getOrder.itemImage),
                           orderQty=orderQty,
                           orderPrice=orderPrice)


@ app.route('/profile/', methods=['GET'])
def profile():

    return render_template('user_pages/profile.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7731, debug=True)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    session(app)
