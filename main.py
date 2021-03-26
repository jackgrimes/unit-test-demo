from utils import volume_of_cylinder

if __name__ == "__main__":
    input_radius = float(input("What is the radius?"))
    input_height = float(input("What is the height?"))
    calculated_volume = volume_of_cylinder(input_radius, input_height)
    print("Calculated volume is {}".format(round(calculated_volume, 2)))
