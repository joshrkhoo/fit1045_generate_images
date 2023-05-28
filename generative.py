
from __future__ import annotations

from ai import predict_number, read_image


def flatten_image(image: list[list[int]]) -> list[int]:
    """
    Flattens a 2D list into a 1D list.
    
    :param image: 2D list of integers representing an image.
    :return: 1D list of integers representing a flattened image.
    """

    # create a new list for the flattened image
    flat_image = []

    # for each number in each row in the matrix, append them to the new list so that we have 1 list
        # append adds each number to the end of the list
    for row in image:   
        for num in row:
            flat_image.append(num)
    return flat_image
  
def unflatten_image(flat_image: list[int]) -> list[list[int]]:
    """
    Unflattens a 1D list into a 2D list.
        
    :param flat_image: 1D list of integers representing a flattened image.
    :return: 2D list of integers.
    """

    # here we square root the length of the flat image to find the length of each row 
    row_size = int(len(flat_image) ** 0.5)

    # here we create a new image with the size of row_size (this is becaue the matrix is a square number)
    # so there are the same number of rows and columns in the matrix
    unflat_image = [[] for _ in range(row_size)]

    for i in range(row_size):
        # populate the unflat_image list with multiples of however large each row is with the numbers from the flat image
        # so if flat image is [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
            #[0, 1, 2, 3, 4, 5] would be in the first row
        # we do this by slicing the flattened image into lengths of however large the square root of row_size is (calculate above)
        # then appending those slices into the rows of the new unflattened list
        unflat_image[i] = flat_image[i * row_size : (i+1) * row_size] 

    return unflat_image

def check_adjacent_for_one(flat_image: list[int], flat_pixel: int) -> bool:
    """
    Checks if a pixel has an adjacent pixel with the value of 1.
    
    :param flat_image: 1D list of integers representing a flattened image.
    :param flat_pixel: Integer representing the index of the pixel in question.
    :return: Boolean.
    """

    row_size = int(len(flat_image) ** 0.5)

    indices_to_check = [flat_pixel - row_size, flat_pixel + row_size]
    
    # here we check if the flat_pixel is on the left edge or not
        # if it is then we dont want to check the one left of it as its not adjacent (left right up or down) to iter
            # thus we dont append it to the list of indices that we need to check are of value 1
        # if it isnt then we add that index to the list to check as it is in fact left of the flat_pixel
    left_of_flat_pixel = flat_pixel-1

    # here we check if the modulo between flat_pixel and row_size is equal to 0
    # we do this as if it is then that means that the flat_pixel is in fact on the left edge
        # in any n x n matrix, the left edges are always multiples of row_size, thus any flat_pixel on the left edge modulo row_size will equate to 0
    if flat_pixel % row_size != 0:
        #here we then add the pixel left of the flat_pixel to check if its value is 1
        indices_to_check.append(left_of_flat_pixel)

    # same format as the left check above but instead we check if the flat_pixel is on the right edge or not
    right_of_flat_pixel = flat_pixel + 1
    
    # here we check if the modulo between flat_pixel and row_size is equal to the row_size - 1 as this is a constant value for each n x n matrices
    # we do this as if it is then that means that the flat_pixel is in fact on the right edge
    # this applies only to the right edges of the matrix
        # in a 5 x 5 matrix the right edges are: 4, 9, 14, 19 
            # if we do 4 % 5, 9 % 5, 14 % 5 and so on the answer will always be 4 (row_size - 1)
    if flat_pixel % row_size != row_size-1:
        #here we then add the pixel right of the flat_pixel to check if its value is 1
        indices_to_check.append(right_of_flat_pixel)


    # values = [flat_image[i] if 0<=i<len(flat_image) else -1 for i in indices]
    # print(indices, values, flat_pixel)


    # here we iterate through the indices_to_check 
    # we first check if its in the range of the flat_image
        # if it isn't then that meants that the indice we are looking to check doesn't exist
        # if it is then we check if the value is == 1
            # return True if it is 
    for i in range(len(indices_to_check)):
        index = indices_to_check[i]
        if index >= 0 and index < len(flat_image):
            if flat_image[index] == 1:
                return True

    return False

def pixel_flip(lst: list[int], orig_lst: list[int], budget: int, results: list, i: int = 0) -> None:
    """
    Uses recursion to generate all possibilities of flipped arrays where
    a pixel was a 0 and there was an adjacent pixel with the value of 1.

    :param lst: 1D list of integers representing a flattened image.
    :param orig_lst: 1D list of integers representing the original flattened image.
    :param budget: Integer representing the number of pixels that can be flipped.
    :param results: List of 1D lists of integers representing all possibilities of flipped arrays, initially empty.
    :param i: Integer representing the index of the pixel in question.
    :return: None.
    """
    
    

    # Base cases
        # when budget is 0 then we cannnot flip anymore 0s
        # when the index is at the end of the list (can't go any further)
    if budget == 0 or i == len(lst):
        return None




    # Recursive case
        #1. check if the index in lst is a 0 and if it is adjacent to a 1
            # if it is then:
                # copy the lst
                # flip the 0 to a 1 
                # append the new copy_lst to results
                    # everytime a 1 is flipped, we first check if the copy_lst with the flipped one is already in results
                        # if it insn't then we add it to results, otherwise we leave it and continue executing
                # from here we then move on to the next index and repeat once the budget 0
            # if it isn't then the code inside the conditional isn't run 

    if lst[i] == 0 and check_adjacent_for_one(orig_lst, i):
        lst_copy = lst[:]
        lst_copy[i] = 1
        if lst_copy not in results:
            results.append(lst_copy)

        # here we pass lst_copy into the function call as we want to check if we can flip another pixel in that same lst (budget > 0)
            # if this is True then another copy_lst is created for that flipped possibility
        pixel_flip(lst_copy, orig_lst, budget - 1, results, i + 1)
    
    # here we just move on to the next index (in the original lst) as the current index in question doesn't have an adjacent 1
    pixel_flip(lst, orig_lst, budget, results, i + 1)

def write_image(orig_image: list[list[int]], new_image: list[list[int]], file_name: str) -> None:
    """
    Writes a newly generated image into a file where the modified pixels are marked as 'X'.
    
    :param orig_image: 2D list of integers representing the original image.
    :param new_image: 2D list of integers representing a newly generated image.
    :param file_name: String representing the name of the file.
    :return: None.
    """
    
    # here we open file_name as 'file'
    with open(file_name, 'w') as file:

        # here we just loop throught the orig_image matrix (both rows and columns) 
            # iterating through every pixel
        for i in range(len(orig_image)):
            for j in range(len(orig_image)):

                # Compare the original image pixel with the new image pixel
                    # If the orig_image is the same as the new_image, we just write any of those two images to the file
                        # in this case we just used new_image
                if orig_image[i][j] == new_image[i][j]:
                    file.write(str(new_image[i][j]))

                # otherwise that means that orig_image[i][j] != new_image[i][j] in a specific pixel 
                # so we mark all flipped pixels 'X'
                else: 
                    file.write('X')

            # here we need to write each row of pixels on a new line otherwise the matrix wont be created
                # this can be seen as it is done inside the first for loop and not the second (i = rows, j = columns)
            file.write('\n')

def generate_new_images(image: list[list[int]], budget: int) -> list[list[list[int]]]:
    """
    Generates all possible new images that can be generated within the budget.
    
    :param image: 2D list of integers representing an image.
    :param budget: Integer representing the number of pixels that can be flipped.
    :return: List of 2D lists of integers representing all possible new images.
    """

    # Flatten the image
    flat_image = flatten_image(image)

    # Get the predicted number for the original image
        # predict_number literally predicts what a number is based on an image of 0s and 1s
        # if we print this line we will get a number
    orig_number = predict_number(image)


    # Initialize an empty list to store the results
    results = []

    # Generate all possible images
    pixel_flip(flat_image, flat_image, budget, results)

    # Initialize an empty list to store the final images
    final_images = []
    

    
    # iterate through each list of images in results
        # unflatten each image
        # then we check if the predicted number of all new_images in results is equal to the orig_number
            # if it is then we append that new image to final_images (images that give the predicted number)
            # basically, we are checking to see the scope of images that the ai 'predict_number' can predict as a specific number
                # so if it were number 4 and we change the image a little bit, can it still say that the number is a 4
    for result in results:
        new_image = unflatten_image(result)
        if predict_number(new_image) == orig_number:
            final_images.append(new_image)
    return final_images



# This function gets the the indexes of each pixel in each image generated that were 0s and flipped to 1s
def get_changed_pixels(original_image, generated_image):

    # here is where we store flipped pixels
    # every image has its own list of flipped pixels     
        # the length of each list depends on if the image uses up the budget and what that budget is
    changed_pixel_index = []

    #flatten both the original image and the generated image
    flat_orig_image = flatten_image(original_image)
    flat_gen_image = flatten_image(generated_image)

    # here we check where the index of each flipped pixel is in each image and then append it to the list created aboce
    for i in range(len(flat_orig_image)):
        if flat_orig_image[i] != flat_gen_image[i]:
            changed_pixel_index.append(i)

    # return the list of flipped pixels
    return changed_pixel_index


if __name__ == "__main__":
    image = read_image("image.txt")
    new_images = generate_new_images(image, 2)
    print(f"Number of new images generated: {len(new_images)}")

    # for gen_image in new_images:
    #     print(get_changed_pixels(image, gen_image))

    # Write first image to test generation
    write_image(image, new_images[0], "new_image_1.txt") 
