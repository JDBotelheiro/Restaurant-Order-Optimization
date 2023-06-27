import streamlit as st
import copy

from datetime import datetime

class Dish:
    def __init__(self, name, complexity):
        self.name = name
        self.complexity = complexity

class Order:
    def __init__(self, order_id, order_time, dishes, source, driver_wait_time):
        self.order_id = order_id
        self.order_time = order_time
        self.dishes = dishes
        self.total_complexity = sum(dish.complexity for dish in dishes)
        self.group_order_id = True if len(dishes) > 3 else False
        self.source = source
        
        if self.source == 'In Restaurant':
            self.driver_wait_time = 0
        else:
            self.driver_wait_time = driver_wait_time
        
        self.updating_order_driver_time = 0
        self.start_time = None
        self.end_time = None
    
    def get_feature_vector(self):
        # For simplicity, let's encode order source as an integer
        source_encoding = 0
        if self.source == 'Bolt Foods':
            source_encoding = 1
        elif self.source == 'UberEats':
            source_encoding = 2
        elif self.source == 'Glovo':
            source_encoding = 3

        # Total complexity of dishes
        total_complexity = sum(dish.complexity for dish in self.dishes)

        # Driver wait time
        wait_time = self.driver_wait_time

        # Return feature vector as a list
        return [source_encoding, total_complexity, wait_time]

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
        
def show_orders(roo, containers, limit=None, num_columns=3):
    orders = roo.orders
    displayed_order_ids = []  # list to keep track of displayed order IDs

    if roo.current_order:
        current_orders_id = [order.order_id for order in roo.current_order]
        orders = [('Doing Order', order) for order in roo.current_order] + orders
    if limit is not None:
        orders = orders[:limit]
    containers = containers.empty()
    with containers.container():
        for i, order_chunk in enumerate(chunks(orders, num_columns)):
            cols = st.columns(num_columns, gap="medium")
            orders_html = "<div class=\"ui centered cards\">"
            for (priority, order), col in zip(order_chunk, cols):
                if order.order_id in displayed_order_ids:  # if order ID has already been displayed, skip this order
                    continue
                displayed_order_ids.append(order.order_id)
                with col:
                    if roo.current_order and order.order_id in current_orders_id:
                        card_color = "mvbackground"
                    else:
                        card_color = "viewbackground"
                    orders_html = f"""
                                    <div class="ui card">   
                                        <div class="content {card_color}">
                                            <div class="header smallheader"># Order {order.order_id}</div>
                                        </div>
                                            <div class="extra content">
                                                <div class="meta" style="text-align: left;"><i class="sort numeric up icon"></i> <strong>Priority Score:</strong> {-round(priority,3) if isinstance(priority, float) else priority}</div>
                                                <div class="meta" style="text-align: left;"><i class="utensils icon"></i> <strong>Dishes:</strong> {", ".join([dish.name for dish in order.dishes])}</div>
                                                <div class="meta" style="text-align: left;"><i class="clock icon"></i> <strong>Total Time to Complete:</strong> {order.total_complexity} min</div>
                                                <div class="meta" style="text-align: left;"><i class="calendar alternate outline icon"></i> <strong>Order time:</strong> {datetime.fromtimestamp(order.order_time).strftime('%Y-%m-%d %H:%M:%S')}</div>
                                                <div class="meta" style="text-align: left;"><i class="shopping cart icon"></i> <strong>Order Type:</strong> {order.source}</div>
                                                <div class="meta" style="text-align: left;"><i class="user clock icon"></i> <strong>Driver wait time:</strong> {round(order.driver_wait_time, 1) if order.source != "In Restaurant" else "N/A"}</div>
                                            </div>
                                    </div>"""
                    orders_html += "</div>"
                    st.markdown(orders_html, unsafe_allow_html=True)
            st.markdown(f"""<br><br>""", unsafe_allow_html=True)
                    
def apply_styles():
    st.markdown(f'<link href="https://cdnjs.cloudflare.com/ajax/libs/semantic-ui/2.4.0/semantic.min.css" rel="stylesheet">', unsafe_allow_html=True)
    with open("styles/style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def update_if_changed(roo, orders_container, previous_orders, previous_current_order):
    """Update orders_container if roo.orders or roo.current_order have changed."""

    if roo.orders != previous_orders or roo.current_order != previous_current_order:
        orders_container.empty()
        show_orders(roo, orders_container)

    # update previous_orders and previous_current_order for the next iteration
    previous_orders = copy.deepcopy(roo.orders)
    previous_current_order = copy.deepcopy(roo.current_order)
    
    return previous_orders, previous_current_order