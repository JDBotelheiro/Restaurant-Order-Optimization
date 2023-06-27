from order_optimization import *
from threading import Thread
from typing import List
import random
import time

def main():
    st.set_page_config(page_title="Order Optimization", layout="wide", page_icon="src/images/mini_logo.png")
    # Define the dishes and their complexities
    dishes: List[Dish] = [Dish('Margherita', 7), Dish('Pepperoni', 10), Dish('Four Cheese', 15), Dish('Vegan', 7), Dish('Supreme', 10), Dish('Mushroom', 8)]

    # Apply custom styles
    apply_styles()

    # Initialize driver_input and orders_input to default values
    driver_input = False
    orders_input = False
    order_priority_input = False
    number_of_orders_value = 2
    
    # Create placeholders
    intro_container = st.empty()
    
    with st.sidebar:
        st.image("src/images/logo.png", )
        st.markdown(f"""<br><br>""", unsafe_allow_html=True)
        number_of_orders = st.empty()
        st.markdown(f"""<br><br>""", unsafe_allow_html=True)
        start_button = st.empty()
        
        if not st.session_state.get('start_button_clicked', False):
            
            number_of_orders_value = number_of_orders.number_input("Number of orders to simulate:", value=15)
            
            if start_button.button('Start'):
                st.session_state['start_button_clicked'] = True
                start_button.empty()
                number_of_orders.empty()
                intro_container.empty()

        if st.session_state.get('start_button_clicked', False):
            st.markdown("<h5><strong>Simulation Configurations:</strong></h5>", unsafe_allow_html=True)
            st.markdown(f"""<br>""", unsafe_allow_html=True)
            driver_input = st.radio("Consider driver's wait time: ", ('Yes', 'No'))
            driver_input = driver_input == 'Yes'
            orders_input = st.radio("Add Weight to Group Orders: ", ('Yes', 'No'))
            orders_input = orders_input == 'Yes'
            order_priority_input = st.radio("Add Weight to Complex Orders: ", ('Yes', 'No'))
            order_priority_input = order_priority_input == 'No'
            
    # Display the introduction text
    if not st.session_state.get('start_button_clicked', False):
        intro_container.markdown("""
        # Order Optimization
        <br>
        Welcome to Order Optimization dashboard. This simulation tool is designed to help us optimize our order handling process, by considering various important factors that influence our service speed and quality.

        Here's how our simulation works:

        1. **Defining the Dishes:** We have a menu of six different dishes with varying complexities. The complexity score represents the time and effort required to prepare the dish.

        2. **Considering the Driver's Wait Time:** If this option is selected, the simulation will take into account the driver's wait time. This is to ensure that we minimize the time our drivers spend waiting for orders to be prepared.

        3. **Weighting Group Orders:** If selected, this option allows the simulation to add more weight to larger orders. This is based on the understanding that larger orders typically require more coordination and preparation time.

        4. **Weighting Complex Orders:** If selected, this option adds additional weight to complex orders. Complex orders are those that contain dishes with a high complexity score. These orders usually take longer to prepare and thus require extra consideration in our optimization process.

        Once these options are selected and the simulation is started, an order optimization algorithm (ROO) is applied. This algorithm takes into consideration the above factors and calculates the most efficient way to handle incoming orders.

        At the end of the simulation, we will have a better understanding of our order handling process and identify areas where we can improve efficiency and service quality.

        Click on the 'Start' button to begin the simulation.
        """, unsafe_allow_html=True)
            
    if st.session_state.get('start_button_clicked', False):
        # Display the app title
        st.title('Dashboard: Bella Napoli Pizzeria 🍕')
        
        # Create an instance of ROO
        roo: ROO = ROO(driver_weight=driver_input, order_group_weight=orders_input, order_priority_weight=order_priority_input)
            
        # Run the restaurant simulation
        run_restaurant_simulation(dishes, roo, number_of_orders_value)






def run_restaurant_simulation(dishes: List[Dish], roo: ROO, number_of_orders: int):
    # Initialize order id
    order_id = 0

    # Initialize Streamlit containers for orders and processing orders©
    st.markdown(f"""<br><br>""", unsafe_allow_html=True)
    processing_order_container = st.empty()
    st.markdown(f"""<br><br>""", unsafe_allow_html=True)
    orders_container = st.empty()
    # Define possible sources of orders
    sources = ['Bolt Foods', 'UberEats', 'Glovo', 'In Restaurant']
    weights = [1.5, 1.5, 1.5, 4.5]
    
    finnish_all_orders = True
    no_more_orders_to_add = True


    while finnish_all_orders:
        # Create a new order with random parameters
        order_dishes = random.sample(dishes, random.randint(1, len(dishes))) 
        driver_wait_time = random.randint(7, 20)  # 5-20 minutes
        order_source = random.choices(sources, weights=weights, k=1)[0]  # randomly select the source of the order
        order = Order(order_id, time.time(), order_dishes, order_source, driver_wait_time)
        #show_orders(roo, orders_container)
        if order_id <= 10 and no_more_orders_to_add:
            # Add the new order to the queue
            roo.add_order(order)
            for _ in range(5):
                show_orders(roo, orders_container)
            
        # Update the priorities and try to start a new order
        roo.optimize_orders()
        show_orders(roo, orders_container)
        random_bool_add_more_orders_weights = [5, 5]
        random_bool_add_more_orders = random.choices([True, False], weights=random_bool_add_more_orders_weights, k=1)[0]
        if random_bool_add_more_orders and order_id > 0:
            roo.start_order()
            # Update the priorities when removing the process order
            roo.optimize_orders()
            for _ in range(5):
                orders_container.empty()
                show_orders(roo, orders_container)            # Clear processing order container and show the processing order
            if roo.current_order:
                #show_orders(roo, orders_container)
                # Find the order with the highest total complexity
                max_complexity_order = max(roo.current_order, key=lambda x: x.total_complexity)
                for i in range(max_complexity_order.total_complexity, -1, -1):
                    for order in roo.current_order:
                        for _ in range(5):
                            orders_container.empty()
                            show_orders(roo, orders_container)
                        # Decrease the complexity of each order by 1, but not lower than 0
                        order.total_complexity = max(0, order.total_complexity - 1)
                    processing_order_container.empty()
                    # Collect all the current order IDs in a list
                    current_order_ids = [order.order_id for order in roo.current_order]

                    # Display the processing message with all the current order IDs and remaining time of the max complexity order
                    processing_order_container.write(f"Processing orders {', '.join([str(order_id) for order_id in current_order_ids])}, remaining time: {i}")
                    show_orders(roo, orders_container)
                    # Update the priorities when removing the process order
                    roo.optimize_orders()
                    # Clear orders container and show all orders
                    show_orders(roo, orders_container)
                    time.sleep(0.6)  # simulate processing time
                # Check the order is finnished
                roo.process_order()
                show_orders(roo, orders_container)
                # Update the priorities when removing the process order
                
                roo.optimize_orders()
                show_orders(roo, orders_container)
        
        # Increase order id
        if order_id <= number_of_orders:
            order_id += 1
        elif order_id > number_of_orders and len(roo.orders) == 0:
            finnish_all_orders = False
        
        if order_id == number_of_orders:
            no_more_orders_to_add = False
            
        # Simulate a delay before the next order comes in
        #show_orders(roo, orders_container)
        for _ in range(5):
            orders_container.empty()
            show_orders(roo, orders_container)
        time.sleep(random.uniform(0.2, 3.5)) 
        orders_container.empty()
        show_orders(roo, orders_container)# wait for a random time before adding the next order
    # Clear orders container and show all orders
    #orders_container.empty()


if __name__ == '__main__':
    main()
