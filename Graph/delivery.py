# Base Data Science snippet
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import time
from tqdm import tqdm_notebook
from scipy.spatial.distance import cdist
import imageio
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from datetime import datetime

plt.style.use("seaborn-dark")

import sys
sys.path.append("../")
from rl.agents.q_agent import QAgent
import geopandas as gpd
#pyproj.datadir.set_data_dir('Users/HP/opt/anaconda3')

# TODO:
    # Now I have to define Q values with journeys. Therefore model can select new paths using that knowledge
    # Time limitations

class DeliveryEnvironment(object):
    def __init__(self, cities, main_data , method, max_box):
            
        print(f"Initialized Delivery Environment with {len(cities)} stops")
        print(f"Target metric for optimization is {method}")

        # Initialization
        self.cities = cities
        self.n_stops = len(cities)
        self.action_space = self.n_stops
        self.observation_space = self.n_stops
        self.max_box = max_box
        self.stops = []
        self.method = method
        self.main_data = main_data
        starting_time = datetime.strptime('2022-03-22 00:00:00','%Y-%m-%d %H:%M:%S') 
        self.current_time = starting_time
        # Generate stops
        #self._generate_constraints(**kwargs)
        self._generate_stops()
        print('generated_stops')
        self._generate_q_values()
        
        self.render()
        
        # Initialize first point
        self.reset()


    def _generate_constraints(self,box_size = 0.2,traffic_intensity = 5):

        if self.method == "traffic_box":

            x_left = np.random.rand() * (self.max_box) * (1-box_size)
            y_bottom = np.random.rand() * (self.max_box) * (1-box_size)

            x_right = x_left + np.random.rand() * box_size * self.max_box
            y_top = y_bottom + np.random.rand() * box_size * self.max_box

            self.box = (x_left,x_right,y_bottom,y_top)
            self.traffic_intensity = traffic_intensity 


    def _generate_stops(self):

        if self.method == "traffic_box":

            points = []
            while len(points) < self.n_stops:
                x,y = np.random.rand(2)*self.max_box
                if not self._is_in_box(x,y,self.box):
                    points.append((x,y))

            xy = np.array(points)
            
        else:
            # Generate geographical coordinates
            #xy = np.random.rand(self.n_stops,2)*self.max_box
            xy = []
            for city in self.cities:
                xy.append([city.city_lng,city.city_lat])

        xy = np.array(xy)
        self.x = xy[:,0]
        self.y = xy[:,1]

    # This state approach is not effective
    def generate_states(self):
        states = []
        city_names = [x.city_name for x in self.cities]
        filtered_dataframe = self.main_data[self.main_data['from'].isin(city_names) & self.main_data['destination'].isin(city_names)]
        
        tupled_list_1 = tuple(zip(filtered_dataframe['from'], filtered_dataframe['departure_time']))
        tupled_list_2 = tuple(zip(filtered_dataframe['destination'], filtered_dataframe['arrival_time']))
        
        main_list = tupled_list_1 + tupled_list_2
        main_list = list(set(main_list))
        
        for location,time in main_list:
            states.append(state(location,time))
        
        return states
        
    def _generate_q_values(self,box_size = 0.2):
        start = time.time()
        # Generate actual Q Values corresponding to time elapsed between two points
        if self.method in ["distance","traffic_box"]:
            xy = np.column_stack([self.x,self.y])
            self.q_stops = cdist(xy,xy)
        elif self.method=="time":
            self.q_stops = np.random.rand(self.n_stops,self.n_stops)*self.max_box
            np.fill_diagonal(self.q_stops,0)
        
   
        elif self.method == "cost":
            
            max_journey_count = 10000 # TEMP 
            self.q_stops = np.ndarray([self.n_stops,self.n_stops,max_journey_count])
            
            
            
            i = 0
            for city_1 in self.cities:
                j = 0
                for city_2 in self.cities:
                    try:
                        q_value = self.main_data.loc[(self.main_data['from'] == city_1.city_name) &
                                               (self.main_data['destination'] == city_2.city_name)]['price']                                                           
                        q_value = list(q_value)  
                    except IndexError as e:
                        q_value = 0
                
                    l = list()
                    
                    for journey_q_value in q_value:
                        l.append(journey_q_value)
                    
                    for ind in range(len(q_value),max_journey_count):    
                        l.append(0)
                        
                        
                    self.q_stops[i,j] = np.array(l)            
                
        end = time.time()        
        print('generated q values in',str(end-start),'seconds')       
        
        #else:
            #raise Exception("Method not recognized")
    
        
    def render(self,return_img = False):
        turkey_map = gpd.read_file('TUR_adm\\tur_polbna_adm2.shp') 
        
        geo_df = gpd.GeoDataFrame(turkey_map)   
        fig, ax = plt.subplots(figsize = (20,18))
        turkey_map.plot(ax=ax,color="gray")
        ax.set_title("Delivery Stops")
        
        # Show stops
        ax.scatter(self.x,self.y,c = "black",s = 50)

        # Show START
        if len(self.stops)>0:
            xy = self._get_xy(initial = True)
            xytext = xy[0]+0.1,xy[1]-0.05
            ax.annotate("START",xy=xy,xytext=xytext,weight = "bold")

        # Show itinerary
        if len(self.stops) > 1:
            ax.plot(self.x[self.stops],self.y[self.stops],c = "blue",linewidth=1,linestyle="--")
            
            # Annotate END
            xy = self._get_xy(initial = False)
            xytext = xy[0]+0.1,xy[1]-0.05
            ax.annotate("END",xy=xy,xytext=xytext,weight = "bold")


        if hasattr(self,"box"):
            left,bottom = self.box[0],self.box[2]
            width = self.box[1] - self.box[0]
            height = self.box[3] - self.box[2]
            rect = Rectangle((left,bottom), width, height)
            collection = PatchCollection([rect],facecolor = "red",alpha = 0.2)
            ax.add_collection(collection)


        plt.xticks([])
        plt.yticks([])
        
        if return_img:
            # From https://ndres.me/post/matplotlib-animated-gifs-easily/
            fig.canvas.draw_idle()
            image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
            image  = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            plt.close()
            return image
        else:
            plt.show()
            
        

    def reset(self):

        # Stops placeholder
        self.stops = []
        self.current_time = datetime.strptime('2022-03-22 00:00:00','%Y-%m-%d %H:%M:%S')
        # Random first stop
        first_stop = np.random.randint(self.n_stops)
        self.stops.append(first_stop)

        return first_stop


    def step(self,destination):
        # initial time : 2022-03-22 00:00:00

        # define a time component here
        
        # Get current state
        state = self._get_state()
        new_state = destination
        # Get reward for such a move
        reward = self._get_reward(state,destination)
    
        # Append new_state to stops
        self.stops.append(destination)
        done = len(self.stops) == self.n_stops

        return new_state,reward,done
    

    def _get_state(self):
        return self.stops[-1]

    def _get_xy(self,initial = False):
        state = self.stops[0] if initial else self._get_state()
        x = self.x[state]
        y = self.y[state]
        return x,y


    def _get_reward(self,state,new_state):
        base_reward = self.q_stops[state,new_state]

        if self.method == "distance":
            return base_reward
        elif self.method == "time":
            return base_reward + np.random.randn()
        elif self.method == "traffic_box":

            # Additional reward correspond to slowing down in traffic
            xs,ys = self.x[state],self.y[state]
            xe,ye = self.x[new_state],self.y[new_state]
            intersections = self._calculate_box_intersection(xs,xe,ys,ye,self.box)
            if len(intersections) > 0:
                i1,i2 = intersections
                distance_traffic = np.sqrt((i2[1]-i1[1])**2 + (i2[0]-i1[0])**2)
                additional_reward = distance_traffic * self.traffic_intensity * np.random.rand()
            else:
                additional_reward = np.random.rand()

            return base_reward + additional_reward
        
        elif self.method == "cost":
            base_reward = self.q_stops[state,new_state]
            not_0_q_values = [x for x in self.q_stops[state,new_state] if x != 0]
            try:
                return not_0_q_values[np.random.randint(len(not_0_q_values))]
            except Exception as e:
                print(e)
    
    @staticmethod
    def _calculate_point(x1,x2,y1,y2,x = None,y = None):

        if y1 == y2:
            return y1
        elif x1 == x2:
            return x1
        else:
            a = (y2-y1)/(x2-x1)
            b = y2 - a * x2

            if x is None:
                x = (y-b)/a
                return x
            elif y is None:
                y = a*x+b
                return y
            else:
                raise Exception("Provide x or y")


    def _is_in_box(self,x,y,box):
        # Get box coordinates
        x_left,x_right,y_bottom,y_top = box
        return x >= x_left and x <= x_right and y >= y_bottom and y <= y_top


    def _calculate_box_intersection(self,x1,x2,y1,y2,box):

        # Get box coordinates
        x_left,x_right,y_bottom,y_top = box

        # Intersections
        intersections = []

        # Top intersection
        i_top = self._calculate_point(x1,x2,y1,y2,y=y_top)
        if i_top > x_left and i_top < x_right:
            intersections.append((i_top,y_top))

        # Bottom intersection
        i_bottom = self._calculate_point(x1,x2,y1,y2,y=y_bottom)
        if i_bottom > x_left and i_bottom < x_right:
            intersections.append((i_bottom,y_bottom))

        # Left intersection
        i_left = self._calculate_point(x1,x2,y1,y2,x=x_left)
        if i_left > y_bottom and i_left < y_top:
            intersections.append((x_left,i_left))

        # Right intersection
        i_right = self._calculate_point(x1,x2,y1,y2,x=x_right)
        if i_right > y_bottom and i_right < y_top:
            intersections.append((x_right,i_right))

        return intersections

class state():
    def __init__(self,location_state,time_state):
        self.location = location_state
        self.time = time_state





def run_episode(env,agent,verbose = 1):

    s = env.reset()
    agent.reset_memory()

    max_step = env.n_stops
    
    episode_reward = 0
    
    i = 0
    while i < max_step:

        # Remember the states
        agent.remember_state(s)

        # Choose an action
        a = agent.act(s)
        
        # Take the action, and get the reward from environment
        s_next,r,done = env.step(a)

        # Tweak the reward
        r = -1 * r
        
        if verbose: print(s_next,r,done)
        
        # Update our knowledge in the Q-table
        agent.train(s,a,r,s_next)
        
        # Update the caches
        episode_reward += r
        s = s_next
        
        # If the episode is terminated
        i += 1
        if done:
            break
            
    return env,agent,episode_reward


class DeliveryQAgent(QAgent):
    
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.reset_memory()

    def act(self,s):
            
        # Get Q Vector
        q = np.copy(self.Q[s,:])

        # Avoid already visited states
        q[self.states_memory] = -np.inf

        if np.random.rand() > self.epsilon:
            a = np.argmax(q)
        else:
            a = np.random.choice([x for x in range(self.actions_size) if x not in self.states_memory])

        return a

    def remember_state(self,s):
        self.states_memory.append(s)

    def reset_memory(self):
        self.states_memory = []
    
        
    # Her adımda aksiyon alacak, bu aksiyon journey seçimi olacak. Bu seçimi yaparken eğer yolculuk zamanı 
    # geçmişse, o act'in ödülü np.inf olacak !!!


def run_n_episodes(env,agent,name="training.gif",n_episodes=1000,render_each=10,fps=10):

    # Store the rewards
    rewards = []
    imgs = []

    # Experience replay
    for i in tqdm_notebook(range(n_episodes)):

        # Run the episode
        env,agent,episode_reward = run_episode(env,agent,verbose = 0)
        rewards.append(episode_reward)
        
        if i % render_each == 0:
            img = env.render(return_img = True)
            imgs.append(img)

    # Show rewards
    plt.figure(figsize = (15,3))
    plt.title("Rewards over training")
    plt.plot(rewards)
    plt.show()

    # Save imgs as gif
    imageio.mimsave(name,imgs,fps = fps)

    return env,agent