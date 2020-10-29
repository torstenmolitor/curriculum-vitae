from Compile import Document, LatexMake
import fitz
from intervaltree import IntervalTree, Interval
import skopt
from skopt import gbrt_minimize
import matplotlib.pyplot as plt
import skopt.plots


DEFAULT_GEOMETRY = {'margin': 2.5, 'top': 2.5, 'bottom': 2.5,
                    'tabcolsep': 5.0, 'parskip': 5.0, 'arraystretch': 1.2,
                    'leftcol': 27, 'rightcol': 73,
                    }


def get_interval_width(interval, points_per_inch=72):
    """
    Helper function to get the width of an intervaltree. Interval
    in inches.
    """
    return (interval.end - interval.begin) / points_per_inch


def params_to_geometry(params):
    """Takes params and builds a dict with the geometry settings"""
    geometry = {}
    for i, var in enumerate(PARAMS_SPACE):
        if var.name == 'col_frac_left':
            leftcol = int(round(100*params[i]))
            geometry['leftcol'] = leftcol
            geometry['rightcol'] = 100 - leftcol
        elif var.name == 'margin':
            geometry['margin'] = params[i]
            geometry['top'] = params[i]
            geometry['bottom'] = params[i]
        else:
            geometry[var.name] = params[i]

    for key in DEFAULT_GEOMETRY:
        if key not in geometry:
            geometry[key] = DEFAULT_GEOMETRY[key]

    return geometry


def layout_cost(params):

    geometry = params_to_geometry(params)
    pdf = DOC.compile(geometry)
    pdf_document = fitz.open(pdf)
    if pdf_document.pageCount > 1:
        return 10

    page1 = pdf_document[-1]
    full_tree_y = IntervalTree()
    tree_y = IntervalTree()
    blks = page1.getTextBlocks()  # Read text blocks of input page
    # Calculate CropBox & displacement
    disp = fitz.Rect(page1.CropBoxPosition, page1.CropBoxPosition)
    croprect = page1.rect + disp
    full_tree_y.add(Interval(croprect[1], croprect[3]))
    for b in blks:  # loop through the blocks
        r = fitz.Rect(b[:4])  # block rectangle
        # add dislacement of original /CropBox
        r += disp
        _, y0, _, y1 = r
        tree_y.add(Interval(y0, y1))
    tree_y.merge_overlaps()
    for i in tree_y:
        full_tree_y.add(i)
    full_tree_y.split_overlaps()
    # For top and bottom margins, we only know they are the first and last elements in the list
    full_tree_y_list = list(sorted(full_tree_y))
    _, bottom_margin = \
        map(get_interval_width, full_tree_y_list[::len(full_tree_y_list) - 1])
    return bottom_margin


PARAMS_SPACE = [
    skopt.space.Real(low=1.0, high=3.0, prior='uniform', name='margin'),
    # skopt.space.Categorical([1.0, 2.0, 4.0], name='margin'),
    # skopt.space.Real(low=2.5, high=2.6, prior='uniform', name='top'),
    # skopt.space.Categorical([1.0, 3.0, 5.0], name='top'),
    # skopt.space.Real(low=1.0, high=2.1, prior='uniform', name='bottom'),
    # skopt.space.Categorical([1.0, 3.0, 5.0], name='bottom'),
    # skopt.space.Real(low=5.0, high=5.1, prior='uniform', name='tabcolsep'),
    # skopt.space.Real(low=1.0, high=7.0, prior='uniform', name='parskip'),
    # skopt.space.Real(low=1.2, high=2.3, prior='uniform', name='arraystretch'),
    skopt.space.Real(low=0.2, high=0.3, prior='uniform', name='col_frac_left'),
]


def tune():
    tune_results = gbrt_minimize(func=layout_cost,
                                 dimensions=PARAMS_SPACE,
                                 # callback=skopt.callbacks.DeltaYStopper(delta=5e-4, n_best=4),
                                 n_calls=20,
                                 )

    best_geometry = params_to_geometry(tune_results.x)

    return best_geometry, tune_results


if __name__ == '__main__':
    DOC = Document()

    best_geometry, tune_results = tune()

    DOC.compile(DEFAULT_GEOMETRY, job_name='cv-default')
    DOC.compile(best_geometry, job_name='cv-optimized')

    lmk = LatexMake()
    lmk.clean()

    print(best_geometry)
    skopt.plots.plot_objective(tune_results)
    plt.show()


