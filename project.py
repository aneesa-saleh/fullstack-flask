from flask import Flask, request, redirect, render_template, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
def home_page():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new_menu_item/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if(request.method == 'POST'):
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        form_complete = bool(name) & bool(price) & bool(description)
        if(form_complete):
            menu_item = MenuItem(name=name, price=price, description=description, restaurant=restaurant)
            session.add(menu_item)
            session.commit()
            flash('{} has been added to the menu'.format(name))
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('new_menu_item.html', restaurant=restaurant)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_item_id>/edit_menu_item/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    if (request.method == 'POST'):
        name = request.form['name']
        price = request.form['price']
        description = request.form['description']
        form_complete = bool(name) & bool(price) & bool(description)
        if (form_complete):
            menu_item.name = name
            menu_item.price = price
            menu_item.description = description
            session.add(menu_item)
            session.commit()
            flash('Changes to {} have been saved'.format(name))

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant=restaurant, menu_item=menu_item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_item_id>/delete_menu_item/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    if (request.method == 'POST'):
        session.delete(menu_item)
        session.commit()
        flash('{} has been deleted from the menu'.format(menu_item.name))

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant.id))
    else:
        return render_template('delete_menu_item.html', restaurant=restaurant, menu_item=menu_item)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
