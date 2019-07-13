import stars
import timeit

def test(iterations=10):
    statement = 'starry_sky.generate_sky()'
    setup = 'starry_sky = stars.Sky()'
    time = timeit.timeit(statement, setup, number=iterations, globals=globals())

    each_iteration = time / iterations
    return each_iteration


if __name__ == '__main__':
    print(test())