# Order Optimization

<p align="center">
  <img src="./src/images/logo.png" alt="Order Optimization">
</p>

This repository contains the source code for a Restaurant Order Optimization system that takes into account various factors to efficiently handle and prepare food orders. The system prioritizes orders based on the complexity of dishes, group orders, driver wait time, and rush hours.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://restaurant-order-optimization.streamlit.app/)


## Repository Structure

The repository consists of the following main components:

- `order_optimization`: The core python script that contains the implementation of the Order Optimization Algorithm.
- `order_simulation`: Python development utilizing reinforcement learning methodologies. It's designed to learn and select the most optimal order through a systematic simulation training process. By continuously interacting with a dynamic environment (the simulated order scenarios), the model progressively improves its decision-making, aiming to achieve the most efficient order handling. (Still on going)
- `app.py`: The Streamlit-based dashboard for visualizing and interacting with the Order Optimization system.
- `src/images/`: Directory containing images used in the application, such as the logo.

## System Requirements

To run this project, you need:

- Python 3.9
- Streamlit 1.24.0

## Setup Instructions

1. Clone the repository: `git clone https://github.com/<your-github-username>/order-optimization.git`
2. Change into the cloned repository's directory: `cd order-optimization`
3. Install necessary Python packages: `pip install -r requirements.txt`
4. Run the Streamlit application: `streamlit run src/app.py`

## Usage

The application starts with a simulation setup where you can choose the number of orders to be simulated. Click 'Start' to begin the simulation. 

Once the simulation starts, you will be asked to select various options:

- **Consider Driver's Wait Time**: If selected, the algorithm will prioritize minimizing the driver's wait time.
- **Add Weight to Group Orders**: If selected, larger orders will be given more priority.
- **Add Weight to Complex Orders**: If selected, orders with complex dishes will be given more priority.

Once the simulation is in progress, you can monitor the prioritization of orders in real-time.

## Contributing

Contributions to this repository are welcome. Please create a new issue to discuss the changes or improvements before creating a pull request.
