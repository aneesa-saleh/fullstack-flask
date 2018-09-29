from flask import Flask, request, redirect, render_template, url_for
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
    page_html = '''
        <!DOCTYPE html>
        <html lang="en">
            <head>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1">
                <title>Restaurants</title>
                <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400" rel="stylesheet">
            </head>
            <body style="font-family: 'Open Sans', sans-serif; font-weight: 300; padding: 10px 20px;">
                <h1>Restaurants</h1>
                <ul style="padding: 0;">
                    {restaurants}
                </ul>
            </body>
        </html>
    '''

    restaurant_html = '''
        <li style="
            list-style-type: none;
            margin: 20px 0;
            box-shadow: 0 0 5px 0 rgba(17,21,0,.2), 0 4px 8px 0 rgba(17,22,0,0.01), 0 8px 50px 0 rgba(17,22,0,.01);
            border-radius: 3px;
            padding: 20px 10px;"
        >
            <a href="/restaurants/{restaurant_id}/" style="color: #0083a8; font-size: 20px; margin-bottom: 5px; text-decoration: none;">
                {restaurant_name}
            </a>
        </li>
    '''

    restaurants = session.query(Restaurant).all()
    restaurants_html = "".join(
        restaurant_html.format(restaurant_name=restaurant.name, restaurant_id=restaurant.id) for restaurant in
        restaurants
    )
    return page_html.format(restaurants=restaurants_html)


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

        return redirect('/restaurants/{restaurant_id}/'.format(restaurant_id=restaurant_id))
    else:
        return render_template('edit_menu_item.html', restaurant=restaurant, menu_item=menu_item)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_item_id>/delete_menu_item/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_item_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_item = session.query(MenuItem).filter_by(id=menu_item_id).one()
    if (request.method == 'POST'):
        session.delete(menu_item)
        session.commit()

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant.id))
    else:
        return render_template('delete_menu_item.html', restaurant=restaurant, menu_item=menu_item)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
