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
from itertools import product

from algorithm import Algorithm

TARGET_RATIO = 2.0/3
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
            print('Unsupported algorithm: {0}'.format(model.algorithm))
    @staticmethod
    def makeCollageRegions(model):
        """Start with the whole area as a region. Each iteration pick the 'worst' region and split it either horizontally
        or vertically at a random point. Remove the old region and add the two new regions.
        
        The worst region is defined to be the region furthest from the TARGET_RATIO.
        """
        def randNearMid(maximum):
            return (randrange(maximum) + randrange(maximum)) // 2
        regions = [(0, 0, model.width, model.height)]
        while len(regions) < model.regionCount:
            worstRegion, worstRegionDiff = RegionMaker.findWorstRegion(regions)
            for region in regions:
                regionDiff = RegionMaker.ratioDiff(region[2], region[3])
                if regionDiff > worstRegionDiff:
                    worstRegion = region
                    worstRegionDiff = regionDiff
            relativeSplitPoint = (randNearMid(worstRegion[2]), randNearMid(worstRegion[3]))
            worstHorizontalSplitDiff = max(RegionMaker.ratioDiff(relativeSplitPoint[0], worstRegion[3]),
                                           RegionMaker.ratioDiff(worstRegion[2]-relativeSplitPoint[0], worstRegion[3]))
            worstVerticalSplitDiff = max(RegionMaker.ratioDiff(worstRegion[2], relativeSplitPoint[1]),
                                         RegionMaker.ratioDiff(worstRegion[2], worstRegion[3]-relativeSplitPoint[1]))
            regions.remove(worstRegion)
            if worstHorizontalSplitDiff < worstVerticalSplitDiff:
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
        if model.regionCount < 5:
            return RegionMaker.makeGridRegions(model)
        width, height = model.width, model.height
        halfWidth, halfHeight = model.width // 2, model.height // 2
        quarterWidth, quarterHeight = model.width // 4, model.height // 4
        centerRegion = (quarterWidth, quarterHeight, halfWidth, halfHeight)
        # Decide where to draw lines near each corner
        bestWorstScore = 999999
        bestRegions = None
        for joinCornerHorizontal in product((True, False), repeat = 4):
            top = (0 if joinCornerHorizontal[0] else quarterWidth,
                   0,
                   halfWidth + (quarterWidth if joinCornerHorizontal[0] else 0) + ((width - halfWidth - quarterWidth) if joinCornerHorizontal[1] else 0),
                   quarterHeight)
            left = (0,
                    quarterHeight if joinCornerHorizontal[0] else 0,
                    quarterWidth,
                    halfHeight + (0 if joinCornerHorizontal[0] else quarterHeight) + (0 if joinCornerHorizontal[2] else (height - halfHeight - quarterHeight)))
            right = (halfWidth + quarterWidth,
                     quarterHeight if joinCornerHorizontal[1] else 0,
                     quarterWidth,
                     halfHeight + (0 if joinCornerHorizontal[1] else quarterHeight) + (0 if joinCornerHorizontal[3] else (height - halfHeight - quarterHeight)))
            bottom = (0 if joinCornerHorizontal[2] else quarterWidth,
                      halfHeight + quarterHeight,
                      halfWidth + (quarterWidth if joinCornerHorizontal[2] else 0) + ((width - halfWidth - quarterWidth) if joinCornerHorizontal[3] else 0),
                      quarterHeight)
            regions = [centerRegion, top, left, right, bottom]
            perimeter = (top[2]//2, right[3], bottom[2], left[3], top[2]-top[2]//2)
            splits = {'top': [0, top[2]], 'right': [0, right[3]], 'bottom': [0, bottom[2]], 'left': [0, left[3]]}
            for i in range(model.regionCount - 5):
                # Find the distance around the perimeter to split a frame
                perimeterDistance = (sum(perimeter) * (i)) // (model.regionCount - 5)
                if perimeterDistance < perimeter[0]:
                    splits['top'].append(perimeterDistance + top[2]//2)
                elif perimeterDistance < sum(perimeter[:2]):
                    perimeterDistance -= perimeter[0]
                    splits['right'].append(perimeterDistance)
                elif perimeterDistance < sum(perimeter[:3]):
                    perimeterDistance -= sum(perimeter[:2])
                    splits['bottom'].append(bottom[2] - perimeterDistance)
                elif perimeterDistance < sum(perimeter[:4]):
                    perimeterDistance -= sum(perimeter[:3])
                    splits['left'].append(left[3] - perimeterDistance)
                else:
                    perimeterDistance -= sum(perimeter[:4])
                    splits['top'].append(perimeterDistance)
            topRegions = []
            for x1, x2 in zip(sorted(splits['top'])[:-1], sorted(splits['top'])[1:]):
                topRegions.append((x1 + top[0], top[1], x2 - x1, top[3]))
            rightRegions = []
            for y1, y2 in zip(sorted(splits['right'])[:-1], sorted(splits['right'])[1:]):
                rightRegions.append((right[0], y1 + right[1], right[2], y2 - y1))
            bottomRegions = []
            for x1, x2 in zip(sorted(splits['bottom'])[:-1], sorted(splits['bottom'])[1:]):
                bottomRegions.append((x1 + bottom[0], bottom[1], x2 - x1, bottom[3]))
            leftRegions = []
            for y1, y2 in zip(sorted(splits['left'])[:-1], sorted(splits['left'])[1:]):
                leftRegions.append((left[0], y1 + left[1], left[2], y2 - y1))
            regions = [centerRegion] + topRegions + rightRegions + bottomRegions + leftRegions
            worstRegion, worstRegionDiff = RegionMaker.findWorstRegion(regions)
            if worstRegionDiff < bestWorstScore:
                bestRegions = regions
                bestWorstScore = worstRegionDiff
        return bestRegions
    @staticmethod
    def findWorstRegion(regions):
        worstRegion = None
        worstRegionDiff = -1
        for region in regions:
            regionDiff = RegionMaker.ratioDiff(region[2], region[3])
            if regionDiff > worstRegionDiff:
                worstRegion = region
                worstRegionDiff = regionDiff
        return worstRegion, worstRegionDiff
    @staticmethod
    def ratioDiff(width, height):
        if width == 0 or height == 0:
            return 0
        return min(abs((width*1.0/height) - TARGET_RATIO), abs((height*1.0/width) - TARGET_RATIO))