// Copyright (C) 2008-2022 Yunshun Chen, Aaron TL Lun, Davis J McCarthy, Matthew E Ritchie, Belinda Phipson, Yifang Hu, Xiaobei Zhou, Mark D Robinson, Gordon K Smyth
// Copyright (C) 2022-2023 Maximilien Colange
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <https://www.gnu.org/licenses/>.

// This file is based on the file 'src/interpolator.h' of the Bioconductor edgeR package (version 3.38.4).


#ifndef INTERPOLATOR_H
#define INTERPOLATOR_H

#include "utils.h"

/* This class just identifies the global maximum in the interpolating function. */

class interpolator {
public:
	interpolator(const size_t&);
	double find_max(const double* x, const double* y);
private:
	const size_t npts;
    std::vector<double> b, c, d;
};


#endif
