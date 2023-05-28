from __future__ import annotations
import unittest
from generative import flatten_image, unflatten_image, check_adjacent_for_one, pixel_flip, write_image, generate_new_images, get_changed_pixels
from ai import read_image


class TestGenerative(unittest.TestCase):
    """Unit tests for the module generative.py"""


    # def tst(self):
    #     mock what you need to mock

    #     expected = something

    #     actual = something

    #     check actual is expected


    def test_flatten_image(self) -> None:
        """
        Verify output of flatten_image for at least three different sizes of images.
        """
        test_image_1x1 = [[0]]

        test_image_3x3 = [
            [1,1,0], 
            [0,0,1], 
            [1,1,0]
            ]


        test_image_5x5 = [
            [0, 1, 1, 0, 0],
            [1, 1, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 1, 1]
            ]


        self.assertEqual(flatten_image(test_image_1x1), [0])
        self.assertEqual(flatten_image(test_image_3x3), [1,1,0,0,0,1,1,1,0])
        self.assertEqual(flatten_image(test_image_5x5), [0,1,1,0,0,1,1,0,0,1,0,1,0,1,0,0,1,1,0,1,0,0,0,1,1])
        
        

    def test_unflatten_image(self) -> None:
        """
        Verify output of unflatten_image for at least three different sizes of flattened images.
        """
        
        test_image_1x1 = [0]
        test_image_3x3 = [1,1,0,0,0,1,1,1,0]
        test_image_5x5 = [0,1,1,0,0,1,1,0,0,1,0,1,0,1,0,0,1,1,0,1,0,0,0,1,1]

        self.assertEqual(unflatten_image(test_image_1x1), [[0]])

        self.assertEqual(unflatten_image(test_image_3x3), [
            [1,1,0], 
            [0,0,1], 
            [1,1,0]
            ])

        self.assertEqual(unflatten_image(test_image_5x5), [
            [0, 1, 1, 0, 0],
            [1, 1, 0, 0, 1],
            [0, 1, 0, 1, 0],
            [0, 1, 1, 0, 1],
            [0, 0, 0, 1, 1]
            ])

    def test_check_adjacent_for_one(self) -> None:
        """
        Verify output of check_adjacent_for_one for three different pixel indexes of an image representing different scenarios.
        """
        test_image =   [0, 1, 1, 
                        0, 0, 0, 
                        1, 0, 0]

        # test middle
        self.assertTrue(check_adjacent_for_one(test_image, 4))

        # test left edge
        self.assertTrue(check_adjacent_for_one(test_image, 3))
        
        # test right edge
        self.assertTrue(check_adjacent_for_one(test_image, 5))

        # test corner
        self.assertFalse(check_adjacent_for_one(test_image, 8))


    def test_pixel_flip(self) -> None:
        """
        Verify output of pixel_flip for a 5x5 image with a budget of 2.
        """
        test_image_5x5 = [
            [0, 1, 0, 1, 0], 
            [1, 1, 1, 0, 1], 
            [1, 1, 1, 1, 0], 
            [1, 1, 1, 1, 1], 
            [0, 0, 1, 1, 0]]

        results = []
        pixel_flip(flatten_image(test_image_5x5), flatten_image(test_image_5x5), 2, results)


        # Verifying number of results
        # there are 8 choose 2 results with a pixel flip of 2 (28)
        # there are 8 choose 1 results with a pixel flip of 1 (8)
            # thus 36 all together
        self.assertEqual(len(results), 36)


        correct_results = [
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0], 
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], 
        [1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0], 
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], 
        [0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0], 
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], 
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1], 
        [0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1]
        ]

        # check if results outputted are in correct_results
        for images in results:
            self.assertTrue(images in correct_results)




    def test_generate_new_images(self) -> None:
        """
        Verify generate_new_images with image.txt and for each image of the generated images verify that:
        - image is of size 28x28,
        - all values in the generated image are either 1s or 0s,
        - the number of pixels flipped from original image are within budget,
        - all pixels flipped from the original image had an adjacent value of 1.
        """
        test_image = read_image('image.txt')

        # generating images with budget of 2 and the image in image.txt
        generate_images = generate_new_images(test_image, 2)



        
        for image in generate_images:
            

            # check length of each 2D image is 28
            self.assertEqual(len(image), 28)
            # checking length of rows of each 2D image is 28
            self.assertTrue(all(len(row) == 28 for row in image))
            
            # check if values of each pixel are 0s or 1s
            for row in image:
                for value in row:
                    #if the value is either 0 or 1 assert True
                    self.assertTrue(value in [0, 1])

            
            # check pixels flipped had an adjacent one by using the def get_changed_pixels
            changed_pixels = get_changed_pixels(test_image, image)
            for pixel in changed_pixels:
                self.assertTrue(check_adjacent_for_one(flatten_image(test_image), pixel))
                
                # Check if number of flipped pixels is within the budget for each pixel
                self.assertFalse(len(changed_pixels) > 2)

                    

if __name__ == "__main__":
    unittest.main()
