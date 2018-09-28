from flask import Flask, request, redirect
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
                    <a href="/r" style="color: #0083a8; font-size: 20px; margin-bottom: 5px;">
                        Home
                    </a>
                    <h1>{name}</h1>
                    <a href="/restaurants/{restaurant_id}/new_menu_item/" style="color: #0083a8; font-size: 20px; margin-bottom: 5px;">
                        Add menu item
                    </a>
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
            <a href="/restaurants/{restaurant_id}/{id}/edit_menu_item/"
                style="display: inline-block; color: #0083a8; font-size: 18px; margin: 10px 0; text-decoration: none;"
            >
                Edit
            </a>
        </li>
        '''
    menu_html = ''.join(
        menu_item_html.format(name=item.name, price=item.price, description=item.description, id=item.id, restaurant_id=restaurant_id)
        for item in items
    )
    return page_html.format(name=restaurant.name, menu=menu_html, restaurant_id=restaurant_id)


# Task 1: Create route for newMenuItem function here

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
        return redirect('/restaurants/{restaurant_id}/'.format(restaurant_id=restaurant_id))
    else:
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
                    <h1>{restaurant_name}</h1>
                    <form style="margin-bottom: 10px;" method="POST" action="/restaurants/{restaurant_id}/new_menu_item/">
                        <h2>Add menu item</h2>
                        <input
                            type="text"
                            name="name"
                            placeholder="Enter name"
                            style="display: block;
                                width: 100%;
                                max-width: 500px;
                                margin-bottom: 10px;
                                font-size: 16px;
                                padding: 5px;
                                border-radius: 3px;
                                border: 1px solid lightgray;"
                        >
                        <input
                            type="text"
                            name="price"
                            placeholder="Enter price"
                            style="display: block;
                                width: 100%;
                                max-width: 500px;
                                margin-bottom: 10px;
                                font-size: 16px;
                                padding: 5px;
                                border-radius: 3px;
                                border: 1px solid lightgray;"
                        >
                        <textarea
                            name="description"
                            placeholder="Enter description"
                            style="display: block;
                                width: 100%;
                                max-width: 500px;
                                margin-bottom: 5px;
                                font-size: 16px;
                                padding: 5px;
                                border-radius: 3px;
                                border: 1px solid lightgray;"
                        ></textarea>
                        <button
                            type="submit"
                            style="font-size: 16px;
                                margin: 10px;
                                background-color: #0083a8;
                                padding: 5px 10px;
                                border: 0;
                                border-radius: 3px;
                                color: white;
                                font-weight: 300;"
                        >Create</button>
                    </form>
                    <a style="color: #0083a8; margin: 5px; font-weight: 400;" href="/restaurants/{restaurant_id}/">
                        Cancel
                    </a>
                </body>
            </html>
        '''
        return page_html.format(restaurant_id=restaurant_id, restaurant_name=restaurant.name)


# Task 2: Create route for editMenuItem function here

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
                        <h1>{restaurant_name}</h1>
                        <form style="margin-bottom: 10px;" method="POST" action="/restaurants/{restaurant_id}/{menu_item_id}/edit_menu_item/">
                            <h2>Edit {menu_item_name}</h2>
                            <input
                                type="text"
                                name="name"
                                placeholder="Enter name"
                                value="{menu_item_name}"
                                style="display: block;
                                    width: 100%;
                                    max-width: 500px;
                                    margin-bottom: 10px;
                                    font-size: 16px;
                                    padding: 5px;
                                    border-radius: 3px;
                                    border: 1px solid lightgray;"
                            >
                            <input
                                type="text"
                                name="price"
                                placeholder="Enter price"
                                value="{menu_item_price}"
                                style="display: block;
                                    width: 100%;
                                    max-width: 500px;
                                    margin-bottom: 10px;
                                    font-size: 16px;
                                    padding: 5px;
                                    border-radius: 3px;
                                    border: 1px solid lightgray;"
                            >
                            <textarea
                                name="description"
                                placeholder="Enter description"
                                style="display: block;
                                    width: 100%;
                                    max-width: 500px;
                                    margin-bottom: 5px;
                                    font-size: 16px;
                                    padding: 5px;
                                    border-radius: 3px;
                                    border: 1px solid lightgray;"
                            >{menu_item_description}</textarea>
                            <button
                                type="submit"
                                style="font-size: 16px;
                                    margin: 10px;
                                    background-color: #0083a8;
                                    padding: 5px 10px;
                                    border: 0;
                                    border-radius: 3px;
                                    color: white;
                                    font-weight: 300;"
                            >Update</button>
                        </form>
                        <a style="color: #0083a8; margin: 5px; font-weight: 400;" href="/restaurants/{restaurant_id}/">
                            Cancel
                        </a>
                    </body>
                </html>
            '''
        return page_html.format(
            restaurant_id=restaurant_id,
            restaurant_name=restaurant.name,
            menu_item_id=menu_item_id,
            menu_item_name=menu_item.name,
            menu_item_price=menu_item.price,
            menu_item_description=menu_item.description
        )


# Task 3: Create a route for deleteMenuItem function here


def delete_menu_item(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
