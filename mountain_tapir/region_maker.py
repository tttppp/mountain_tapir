# -*- coding: utf-8 -*-
#
# Mountain Tapir Collage Maker is a tool for combining images into collages.
# Copyright (c) 2016, tttppp
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from math import sqrt
from random import randrange

from algorithm import Algorithm

TARGET_RATIO = 2/3
UNACCEPTABLE_WIDTH=50
UNACCEPTABLE_HEIGHT=50

class RegionMaker:
    """A region is a tuple (left, top, width, height)."""
    @staticmethod
    def makeRegions(model):
        """Split the preview pane into disjoint regions."""
        if model.algorithm == Algorithm.COLLAGE:
            return RegionMaker.makeCollageRegions(model)
        elif model.algorithm == Algorithm.GRID:
            return RegionMaker.makeGridRegions(model)
        elif model.algorithm == Algorithm.FRAME:
            return RegionMaker.makeFrameRegions(model)
        else:
            print('Unsupported algorithm: {}'.format(model.algorithm))
    @staticmethod
    def makeCollageRegions(model):
        """Start with the whole area as a region. Each iteration pick the 'worst' region and split it either horizontally
        or vertically at a random point. Remove the old region and add the two new regions.
        
        The worst region is defined to be the region furthest from the TARGET_RATIO.
        """
        def ratioDiff(width, height):
            if width == 0 or height == 0:
                return 0
            return min(abs((width*1.0/height) - TARGET_RATIO), abs((height*1.0/width) - TARGET_RATIO))
        def randNearMid(maximum):
            return (randrange(maximum) + randrange(maximum)) // 2
        regions = [(0, 0, model.width, model.height)]
        while len(regions) < model.regionCount:
            worstRegion = None
            worstRegionDiff = -1
            for region in regions:
                regionDiff = ratioDiff(region[2], region[3])
                if regionDiff > worstRegionDiff:
                    worstRegion = region
                    worstRegionDiff = regionDiff
            relativeSplitPoint = (randNearMid(worstRegion[2]), randNearMid(worstRegion[3]))
            worstHorizontalSplitDiff = max(ratioDiff(relativeSplitPoint[0], worstRegion[3]),
                                           ratioDiff(worstRegion[2]-relativeSplitPoint[0], worstRegion[3]))
            worstVerticalSplitDiff = max(ratioDiff(worstRegion[2], relativeSplitPoint[1]),
                                         ratioDiff(worstRegion[2], worstRegion[3]-relativeSplitPoint[1]))
            regions.remove(worstRegion)
            if worstHorizontalSplitDiff > worstVerticalSplitDiff:
                # Split vertically
                regions.append((worstRegion[0], worstRegion[1], relativeSplitPoint[0], worstRegion[3]))
                regions.append((worstRegion[0]+relativeSplitPoint[0], worstRegion[1], worstRegion[2]-relativeSplitPoint[0], worstRegion[3]))
            else:
                # Split horizontally
                regions.append((worstRegion[0], worstRegion[1], worstRegion[2], relativeSplitPoint[1]))
                regions.append((worstRegion[0], worstRegion[1]+relativeSplitPoint[1], worstRegion[2], worstRegion[3]-relativeSplitPoint[1]))
            # Restart if any width or height is unacceptable
            if regions[-2][2] <= UNACCEPTABLE_WIDTH or regions[-2][3] <= UNACCEPTABLE_HEIGHT or regions[-1][2] <= UNACCEPTABLE_WIDTH or regions[-1][3] <= UNACCEPTABLE_HEIGHT:
                regions = [(0, 0, model.width, model.height)]
        return regions
    @staticmethod
    def makeGridRegions(model):
        shortSide = int(sqrt(model.regionCount))
        while model.regionCount % shortSide != 0:
            shortSide -= 1
        longSide = model.regionCount // shortSide
        if model.width > model.height:
            columns = longSide
            rows = shortSide
        else:
            columns = shortSide
            rows = longSide
        # Need to set width and height of each cell programmatically to avoid rounding errors in calculation of cellWidth and cellHeight
        return [(x*model.width//columns,
                 y*model.height//rows,
                 (x+1)*model.width//columns - x*model.width//columns,
                 (y+1)*model.height//rows - y*model.height//rows)
                for x in range(columns) for y in range(rows)]
    @staticmethod
    def makeFrameRegions(model):
        return []
