from flask import Flask
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
        restaurant_html.format(restaurant_name=restaurant.name, restaurant_id=restaurant.id) for restaurant in restaurants
    )
    return page_html.format(restaurants=restaurants_html)

@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
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
                    <a href="/" style="color: #0083a8; font-size: 20px; margin-bottom: 5px;">
                        Home
                    </a>
                    <h1>{name}</h1>
                    <ul style="padding: 0;">
                        {menu}
                    </ul>
                </body>
            </html>
        '''
    menu_item_html = '''
        <li style="
            list-style-type: none;
            margin: 20px 0;
            box-shadow: 0 0 5px 0 rgba(17,21,0,.2), 0 4px 8px 0 rgba(17,22,0,0.01), 0 8px 50px 0 rgba(17,22,0,.01);
            border-radius: 3px;
            padding: 20px 10px;"
        >
            <span style="display: block; font-weight: 400; font-size: 22px; margin-bottom: 10px;">{name}</span>
            <span style="display: block; font-size: 16px; margin-bottom: 10px;">Price: {price}</span>
            <span style="display: block; font-size: 18px;">{description}</span>
        </li>
        '''
    menu_html = ''.join(
        menu_item_html.format(name=item.name, price=item.price, description=item.description) for item in items
    )
    return page_html.format(name=restaurant.name, menu=menu_html)

# Task 1: Create route for newMenuItem function here


def new_menu_item(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here


def edit_menu_item(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here


def delete_menu_item(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)