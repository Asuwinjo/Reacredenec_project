#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install flask')


# In[ ]:


from flask import Flask, render_template, request, redirect


# In[ ]:


get_ipython().system('pip install flask_sqlalchemy')


# In[ ]:


from flask_sqlalchemy import SQLAlchemy


# In[ ]:


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///billing.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# In[ ]:


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Srting(80), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(120))
    
    def __repr__(self):
        return f'<Item{self.name}>'
    
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)
    
@app.route('/item/add', methods=['GET','POST'])
def add_item():
    if request.method == 'POST':
        new_item = Item(
        name = request.form['name'],
        price = request.form['price'],
        description = request.form['description']
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_item.html')

@app.route('/items/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    Item = Item.query.get_or_404(item_id)
    if request.method == 'POST':
        Item.name = request.form['name']
        Item.price = request.form['price']
        Item.description = request.form['description']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_item.html', item=Item)

@app.route('/items/delete/<int:item_id>', methods=['GET','POST'])
def delete_item(item_id):
    Item = Item.query.get_or_404(item_id)
    db.session.delete(Item)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/bill', methods=['GET', 'POST'])
def generate_bill():
    if request.method == 'POST':
        item_ids = request.form.getlist('item_ids')
        items = query.filter(Item.id.in_(item_ids)).all()
        cost = sum(item.price for item in items)
        return render_template('bill.html', items=items, cost=cost)
    items = Item.query.all()
    return render_template('Generate_bill.html', items=items)


# In[ ]:


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

