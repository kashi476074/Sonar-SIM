import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

class HalfCircleSonar:
    collision = False

    def __init__(self, arena_size=100, steps=500, speed=1): #Change the durition by steps
        self.arena_size = arena_size
        self.steps = steps
        self.speed = speed
        self.source_pos = np.array([arena_size - 22, arena_size // 2]) #Position of Source or ship
        self.target_pos = np.array([10, arena_size // 2])   #Position of Target or submarine
        self.wave_radius = 0
        self.wave_center = self.source_pos
        self.time_taken = 0  # Variable to track time taken
        self.distance = 0  # Variable to track distance traveled
        self.time_text = None

        # Load background image
        self.background_img = plt.imread('sea.jpg') 

        self.fig, self.ax = plt.subplots(figsize=(10, 10))  # Adjust figsize for vertical orientation
        self.ax.set_title("Sonar Demo")
        self.ax.grid(False)  # Remove grids
        self.ax.imshow(self.background_img, extent=[0, arena_size, 0, arena_size])  # Set background image

        # Load source and target images
        self.source_img = plt.imread('ship.png')
        self.target_img = plt.imread('sub.png')

        # Plot source and target images
        self.ax.imshow(self.source_img, extent=[self.source_pos[1] - 5, self.source_pos[1] + 10,
                                                 self.source_pos[0] - 5, self.source_pos[0] + 10]) #[x_min, x_max, y_min, y_max]

        self.ax.imshow(self.target_img, extent=[self.target_pos[1] - 5, self.target_pos[1] + 5,
                                                 self.target_pos[0] - 5, self.target_pos[0] + 5])#[x_min, x_max, y_min, y_max]

        self.wave, = self.ax.plot([], [], color='red', linestyle='dashed', label='Wave')

        self.time_text = self.ax.text(0.02, 0.95, '', transform=self.ax.transAxes)  # Text for displaying time
        self.ax.legend()

        self.ani = animation.FuncAnimation(self.fig, self.update, frames=self.steps, interval=50, blit=False)

    def update(self, num):
        if self.collision == False:
            # Expand the wave radius
            if self.wave_radius < self.arena_size:
                self.wave_radius += self.speed

            # Update the wave circle from source to target
            self.wave.set_data(*self.source_circle_points(self.wave_center, self.wave_radius))

            # Check for collision with the target
            if np.linalg.norm(self.wave_center - self.target_pos) <= self.wave_radius:
                self.collision = True
                # Calculate time taken to reach target
                self.time_taken = num * 0.06  # Assuming 50 ms interval
                self.distance = self.speed * self.time_taken  # Calculate distance
                self.wave_radius = 0
                self.wave_center = self.target_pos
        else:
            # Expand the wave radius from target to source
            if self.wave_radius < self.arena_size:
                self.wave_radius += self.speed

            # Update the wave circle from target to source
            self.wave.set_data(*self.target_circle_points(self.wave_center, self.wave_radius))

            # Check for collision with source
            if np.linalg.norm(self.wave_center - self.source_pos) <= self.wave_radius:
                self.collision = False
                self.time_taken += num * 0.06  # Add time taken to return to source
                self.distance += self.speed * (num * 0.05)  # Add distance traveled during return
                self.wave_radius = 0
                self.wave_center = self.source_pos
                #  adjust the Distance formula here Distance=Speed of Sound×Time
                self.time_text.set_text(f'Time taken: {self.time_taken:.2f} seconds\nDepth : {((self.time_taken/3600)*3315)/2 :.2f} miles')

        # Update time text

        return self.wave, self.time_text

    def save_animation(self, filename='time_distance.mp4'):
        self.ani.save(filename, writer='ffmpeg')

    def source_circle_points(self, center, radius, num_points=100):
        theta = np.linspace(np.pi, 2*np.pi, num_points)  # Change theta range for vertical orientation
        x = center[1] + radius * np.cos(theta)  # Swap x and y coordinates
        y = center[0] + radius * np.sin(theta)  # Swap x and y coordinates
        return x, y

    def target_circle_points(self, center, radius, num_points=100):
        theta = np.linspace(0, np.pi, num_points)  # Change theta range for vertical orientation
        x = center[1] + radius * np.cos(theta)  # Swap x and y coordinates
        y = center[0] + radius * np.sin(theta)  # Swap x and y coordinates
        return x, y

def main():
    sim = HalfCircleSonar(steps=200)  # Increase the number of steps for longer simulation
    sim.save_animation('time_distance.mp4')
    plt.show()

if __name__ == "__main__":
    main()
