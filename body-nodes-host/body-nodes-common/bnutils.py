#
# MIT License
# 
# Copyright (c) 2024 Manuel Bottini
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


class BnReorientAxis:
    def __init__( self ):
        self.reorientAxis = [0, 1, 2, 3]
        self.reorientSign = [1, 1, 1, 1]

    # Change the orientation of received data to align to the main application
    # ioAxis is an array of 3 or 4 integer that can be 0 ('w'), 1 ('x'), 2 ('y'), or 3 ('z').
    # Example [ 0, 1, 2, 3]
    # ioSign is an array of 3 or 4 integers that can be 1 or -1. Example [1, 1, 1, 1]
    # Note: by default the orientation is set as [ 0, 1, 2, 3 ] and [1, 1, 1, 1]
    def config( self, ioAxis, ioSign ):
        self.reorientAxis = ioAxis
        self.reorientSign = ioSign

    def apply( self, iovalues ):
        ovalues = []
        for idv in range(0, len(iovalues)):
            ovalues.append( iovalues[ self.reorientAxis[idv] ] * self.reorientSign[idv]  )
        for idv in range(0, len(iovalues)):
            iovalues[idv] = ovalues[idv]




if __name__ == "__main__":
    print("Testing BnReorientAxis")

    test_io_axis = [ 3, 2, 1, 0 ]
    test_io_sign = [ -1, -1, -1, -1 ]
    test_ivalues = [ 3, 4.5, 2, 10.2 ]
    # ovalues are equal to ivalues for inplace operators
    test_ovalues = [ 3, 4.5, 2, 10.2 ]
    test_evalues = [ -10.2, -2, -4.5, -3 ]
    test_obj = BnReorientAxis()
    test_obj.config( test_io_axis, test_io_sign )
    test_obj.apply( test_ovalues )
    if test_evalues == test_ovalues:
        print("Test passed: output = "+str(test_ovalues) + " expected = "+str(test_evalues))
    else:
        print("Test failed: output = "+str(test_ovalues) + " expected = "+str(test_evalues))





