import time
import heapq
import math

class ROO:

    def __init__(self, driver_weight, order_group_weight, order_priority_weight, buffer_time_percentage = 0.1):
        self.orders = []
        self.current_order = None
        self.buffer_time_percentage = buffer_time_percentage
        self.driver_weight = driver_weight
        self.order_group_weight = order_group_weight
        self.order_priority_weight = order_priority_weight

    def calculate_order_priority(self, order):
        wait_time = time.time() - order.order_time
        
        # Consider driver's wait time
        if order.source != 'In Restaurant' and self.driver_weight:
            if order.driver_wait_time > order.total_complexity:
                order.updating_order_driver_time += (order.driver_wait_time - order.total_complexity) / 100
                wait_time -= (order.driver_wait_time - order.total_complexity) / 100
            if order.updating_order_driver_time > 0 and order.driver_wait_time < order.total_complexity:
                wait_time += order.updating_order_driver_time
                order.updating_order_driver_time = 0
            if order.driver_wait_time > 0:
                order.driver_wait_time -= .05
                
        if order.group_order_id and self.order_group_weight:
            wait_time *= 1.1  # 1% more priority for group orders
            
        #buffer_time = order.total_complexity * self.buffer_time_percentage

        # Factor for time of day (rush hour)
        current_hour = time.localtime().tm_hour
        if 12 <= current_hour <= 14 or 18 <= current_hour <= 20:  # peak hours
            wait_time *= 1.1
            
        if self.order_priority_weight:
            priority = -1 * (wait_time) / math.log(order.total_complexity + 1)
        else:
            priority = -1 * (wait_time) / math.exp((1/order.total_complexity) + 1)
        return priority
    
    
    def add_order(self, order):
        heapq.heappush(self.orders, (self.calculate_order_priority(order), order))

    def priority_closeness(self, priority1, priority2):
        # This could be as simple as taking the absolute difference between their priorities
        return abs(priority1 - priority2)

    def dishes_in_common(self, order1, order2):
        # This checks if the intersection of their sets of dishes is non-empty and not more than 3
        common_dishes = len(set(order1.dishes) & set(order2.dishes))
        if len(order1.dishes) > len(order2.dishes):
            min_len_order = len(order2.dishes)
        else:
            min_len_order = len(order1.dishes)
        return 0 < common_dishes <= 3 and common_dishes == min_len_order
    
    def start_order(self, threshold = 2):
        if self.orders and not self.current_order:
            # Start with the highest priority order
            priority, order = heapq.heappop(self.orders)

            # Create a group of orders, starting with the highest priority one
            group_orders = [order]

            # Create a new list to hold orders that we'll put back in the heap later
            leftover_orders = []

            while self.orders:
                potential_priority, potential_order = heapq.heappop(self.orders)
                if self.priority_closeness(priority, potential_priority) <= threshold and self.dishes_in_common(order, potential_order):
                    # Add this order to the group
                    group_orders.append(potential_order)
                    break

                else:
                    # This order doesn't meet the criteria, so we'll put it back later
                    leftover_orders.append((potential_priority, potential_order))
                    
            # Put the leftover orders back in the heap
            for leftover_order in leftover_orders:
                # Check if the order_id of the leftover_order is not already present in the self.orders
                order_ids = [order.order_id for _, order in self.orders]
                if leftover_order[1].order_id not in order_ids:
                    heapq.heappush(self.orders, leftover_order)
                else:
                    print(f"Order {leftover_order[1].order_id} is already in the list, skipping...")

            # Start the group of orders
            self.current_order = group_orders

    def process_order(self, choose_order = None):
        # Get the order with the highest total complexity
        max_complexity_order = max(self.current_order, key=lambda x: x.total_complexity)

        # Process one unit of complexity per time unit
        if max_complexity_order.total_complexity > 0:
            max_complexity_order.total_complexity -= 1
        else:
            self.complete_order(max_complexity_order.order_id)

    def complete_order(self, order_id):
        # Get the order from current_order list with given order_id
        completed_order = next((order for order in self.current_order if order.order_id == order_id), None)
        
        if completed_order:
            # Remove the completed order from the current_order list
            self.current_order.remove(completed_order)
            
    def optimize_orders(self):
        self.orders = [(self.calculate_order_priority(order_obj), order_obj) for _, order_obj in self.orders]
        # Re-heapify orders
        heapq.heapify(self.orders)

        # If you want to get all orders in sorted order (from highest to lowest priority), you can use heapq.nsmallest:
        self.orders = heapq.nsmallest(len(self.orders), self.orders)

    def modify_order(self, order_id, new_dishes=None, driver_wait_time=None):
        # Find the order
        for i in range(len(self.orders)):
            if self.orders[i][1].order_id == order_id:
                if new_dishes is not None:
                    # Update dishes and total complexity
                    self.orders[i][1].dishes = new_dishes
                    self.orders[i][1].total_complexity = sum(dish.complexity for dish in new_dishes)
                if driver_wait_time is not None:
                    # Update driver wait time
                    self.orders[i][1].driver_wait_time = driver_wait_time
                break
        # Re-optimize orders after modification
        self.optimize_orders()
