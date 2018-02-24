"""Problem 103: Stacking boxes."""

class Box(object):
    """A Box may have boxes inside."""
    def __init__(self, name, dimensions):
        """New Box with name, dimensions and no children."""
        self.name = name
        self.dimensions = sorted(dimensions)
        self.children = []

    def add(self, box):
        """See if box fits in my subtree."""
        if not self.contains(box):
            return False
        else:
            placed = False
            for child in self.children:
                if child.add(box):
                    placed = True
                elif child.equal_dimensions(box):
                    placed = True
            if not placed:
                self.children.append(box)
            return True

    def contains(self, box):
        """Get if box fits in self?"""
        for i, dim_i in enumerate(self.dimensions):
            if dim_i <= box.dimensions[i]:
                return False
        return True

    def max_length(self):
        """Get the longest path of sub-boxes."""
        longest = 0
        longest_path = ''
        for child in self.children:
            child_len, child_path = child.max_length()
            if child_len > longest:
                longest = child_len
                longest_path = child_path
        return self._result_max_length(longest, longest_path)

    def _result_max_length(self, longest, longest_path):
        if longest_path:
            path = longest_path + ' ' + self.name
        else:
            path = self.name
        return longest + 1, path

    def __str__(self):
        return self.name + '[' + ', '.join([str(child) for child in self.children]) + ']'

    def equal_dimensions(self, box):
        """Check if they are "same box"."""
        return self.dimensions == box.dimensions

class Hood(Box):
    """Hood is a Box without own propierties. Only for its children."""
    def __init__(self):
        """Create an empty Hood."""
        super(Hood, self).__init__('hood', [])

    def contains(self, box):
        return True

    def _result_max_length(self, longest, longest_path):
        return longest, longest_path

    def equal_dimensions(self, box):
        return False

def main(inp):
    """Read input, solve it and return output."""
    result = []
    while inp:
        inp, outp = stack_boxes(inp)
        result.append(outp)
    return "".join(result)


def sort_boxes(boxes, left, right):
    """Sort the sub-list of boxes within left and right."""
    if left >= right:
        return
    box = boxes[right]
    sep_left = left
    sep_right = right
    while True:
        while is_bigger(boxes[sep_left], box) and sep_left < sep_right:
            sep_left += 1
        while is_bigger(box, boxes[sep_right]) and sep_right > sep_left:
            sep_right -= 1
        if sep_left >= sep_right:
            sep = sep_right
            break
        aux = boxes[sep_left]
        boxes[sep_left] = boxes[sep_right]
        boxes[sep_right] = aux
    sep = sep_left
    assert boxes[sep] == box, (boxes, sep_left, sep_right)
    sort_boxes(boxes, left, sep - 1)
    sort_boxes(boxes, sep + 1, right)
    return


def is_bigger(box1, box2):
    """Get if box1 is bigger than box2."""
    for i, dim_i in enumerate(box1[1]):
        if dim_i > box2[1][i]:
            return True
        if dim_i < box2[1][i]:
            return False
    return box1[0] < box2[0]


def stack_boxes(inp):
    """Solve one problem and return solution and next problems."""
    first_row, rest = inp.split('\n', 1)
    k, num_dims = first_row.split(' ')
    k = int(k)
    num_dims = int(num_dims)
    data = rest.split('\n', k)
    boxes_def = data[:k]
    rest = data[k]
    boxes = []
    for i, box_def in enumerate(boxes_def, 1):
        box_def_split = sorted(map(int, box_def.split(' ')))
        assert len(box_def_split) == num_dims, (box_def_split, num_dims)
        boxes.append((i, box_def_split))
    sort_boxes(boxes, 0, len(boxes) - 1)  # Quicksort
    my_hood = Hood()
    for box in boxes:
        my_hood.add(Box(str(box[0]), box[1]))
    max_length, max_path = my_hood.max_length()
    result = "{}\n{}\n".format(max_length, max_path)
    return rest, result

def read_all_input():
    """Return all lines from prompt."""
    data_read = ""
    finished = False
    while not finished:
        try:
            data_read += raw_input("") + '\n'
        except EOFError:
            finished = True
    return data_read


def _main():
    _main_input = read_all_input()
    _main_result = main(_main_input)
    print _main_result


if __name__ == '__main__':
    _main()
