# Author: Hauxu Yu

# A module for feature/peak detection

# Import modules
import numpy as np
from tqdm import tqdm
from scipy.signal import argrelextrema
from .msms import spec_similarity
import copy


def roi_finder(d, params, **kwargs):
    """
    A function to find the region of interest (ROI) in the MS data.

    Parameters
    ----------------------------------------------------------
    d: MSData object
        An MSData object that contains the MS data.
    params: Params object
        A Params object that contains the parameters.
    """

    # A list to store the rois in progress
    rois = []
    # A list for finally selected ROIs
    final_rois = []

    # Initiate a set of rois using the first MS1 scan
    fs = d.scans[d.ms1_idx[0]]    # The first scan

    # Find the MS2 for this scan
    allocate_vec = loc_ms2_for_ms1_scan(d, d.ms1_idx[0])

    for i in range(len(fs.int_seq)):
        roi = Roi(scan_idx=d.ms1_idx[0], rt=fs.rt, mz=fs.mz_seq[i], intensity=fs.int_seq[i])
        if allocate_vec[i] > 0:
            roi.ms2_seq.append(d.scans[allocate_vec[i]])
        rois.append(roi)
    
    last_ms1_idx = d.ms1_idx[0]
    last_rt = fs.rt

    # Loop over all MS1 scans
    for ms1_idx in tqdm(d.ms1_idx[1:]):

        s = d.scans[ms1_idx]    # The current MS1 scan

        # Find the MS2 for this scan
        allocate_vec = loc_ms2_for_ms1_scan(d, ms1_idx)

        visited_idx = []    # A list to store the visited indices of ions in the current MS1 scan
        visited_rois_idx = []   # A list to store the visited indices of rois

        # Loop over all current rois
        for i, roi in enumerate(rois):
            mz_diff = np.abs(roi.mz - s.mz_seq)
            if np.min(mz_diff) < params.mz_tol_ms1:
                min_idx = np.argmin(mz_diff)
                if min_idx not in visited_idx:
                    roi.extend_roi(scan_idx=ms1_idx, rt=s.rt, mz=s.mz_seq[min_idx], intensity=s.int_seq[min_idx])
                    roi.gap_counter = 0
                    if allocate_vec[min_idx] > 0:
                        roi.ms2_seq.append(d.scans[allocate_vec[min_idx]])
                    visited_idx.append(min_idx)
                    visited_rois_idx.append(i)

        to_be_moved = []
        # Plus one to the gap counter of the rois that are not visited
        for i in range(len(rois)):
            if i not in visited_rois_idx:
                rois[i].extend_roi(scan_idx=ms1_idx, rt=s.rt, mz=np.nan, intensity=0)
                rois[i].gap_counter = rois[i].gap_counter + 1
                if rois[i].gap_counter > params.roi_gap:
                    to_be_moved.append(i)
        
        # Move the rois that have not been visited for a long time to final_rois
        for i in to_be_moved[::-1]:
            final_rois.append(rois.pop(i))
        
        # Create new rois for the rest
        for i in range(len(s.int_seq)):
            if i not in visited_idx:
                # Add a zero before the new roi
                roi = Roi(scan_idx=last_ms1_idx, rt=last_rt, mz=np.nan, intensity=0)
                roi.extend_roi(scan_idx=ms1_idx, rt=s.rt, mz=s.mz_seq[i], intensity=s.int_seq[i])
                roi.mz = s.mz_seq[i]
                if allocate_vec[i] > 0:
                    roi.ms2_seq.append(d.scans[allocate_vec[i]])
                rois.append(roi)

        last_ms1_idx = ms1_idx
        last_rt = s.rt
           
    # Move all rois to final_rois
    for roi in rois:
        final_rois.append(roi)

    for roi in final_rois:
        roi.sum_roi()
    
    return final_rois


def find_roi_cut(roi, params, **kwargs):
    """
    A function to find place to cut an roi based on ion identity.
    An roi will be cut only if it has
    - params.min_ion_num or more non-zero intensities
    - two or more MS/MS spectra

    Parameters
    ----------------------------------------------------------
    roi: Roi object
        An Roi object that contains the roi.
    params: Params object
        A Params object that contains the parameters.
    """

    # counter the number of non-zero intensities in the roi
    non_zero_int = np.count_nonzero(roi.int_seq)

    if non_zero_int >= params.min_ion_num and len(roi.ms2_seq) >= 2:

        cut_positions = argrelextrema(np.array(roi.int_seq), np.less)[0]
        final_cut_positions = []

        if len(cut_positions) != 0:
            # determine if a potential cut point should be really cut
            # compare the MS2 spectra on the left and right
            
            # add a zero and len(int_seq) to cut_positions
            cut_positions = np.insert(np.array([0, len(roi.int_seq)-1]), 1, cut_positions)

            for i in range(len(cut_positions)-2):
                scan_idx1 = roi.scan_idx_seq[i]
                scan_idx2 = roi.scan_idx_seq[i+1]
                scan_idx3 = roi.scan_idx_seq[i+2]

                ms2_left = []
                ms2_right = []

                for j in range(len(roi.ms2_seq)):
                    if roi.ms2_seq[j].scan > scan_idx1 and roi.ms2_seq[j].scan < scan_idx2:
                        ms2_left.append(roi.ms2_seq[j])
                    if roi.ms2_seq[j].scan > scan_idx2 and roi.ms2_seq[j].scan < scan_idx3:
                        ms2_right.append(roi.ms2_seq[j])

                if len(ms2_left) != 0 and len(ms2_right) != 0:
                    dp = spec_similarity(spec1=ms2_left[-1], spec2=ms2_right[0], 
                                         mz_tol=params.mz_tol_ms2)
                    # if dp is a float
                    if isinstance(dp, float):
                        if dp < params.ms2_sim_tol:
                            final_cut_positions.append(cut_positions[i+1])
        
        # cut the roi
        if len(final_cut_positions) != 0:
            return final_cut_positions
        else:
            return None
    else:
        return None


def roi_cutter(roi, positions):
    """
    A function to cut a long roi by given positions.

    Parameters
    ----------------------------------------------------------
    roi: Roi object
        An Roi object that contains the roi.
    positions: list
        A list of positions to cut the roi.
    """

    # add a zero and len(int_seq) to positions
    positions = np.insert(np.array([0, len(roi.int_seq)-1]), 1, positions)

    rois = []

    for i in range(len(positions)-1):
        fst = positions[i]
        snd = positions[i+1]
        temp = copy.deepcopy(roi)
        temp.subset_roi(fst, snd)
        rois.append(temp)

    return rois
    

def loc_ms2_for_ms1_scan(d, ms1_idx, **kwargs):
    """
    A function to allocate MS2 scans for the ions in a given MS1 scan.

    Parameters
    ----------------------------------------------------------
    d: MSData object
        An MSData object that contains the MS data.
    ms1_idx: int
        The index of the MS1 scan.
    """

    allocate_vec = np.zeros(len(d.scans[ms1_idx].int_seq), dtype=int) - 1
    mz_vec = d.scans[ms1_idx].mz_seq

    for i in range(ms1_idx+1, len(d.scans)):
        if d.scans[i].level == 1:
            break
        if d.scans[i].level == 2:
            mz_diff = np.abs(mz_vec - d.scans[i].precs_mz)
            allocate_vec[np.argmin(mz_diff)] = i

    return allocate_vec


class Roi:
    """
    A class to store a region of interest (ROI).
    """

    def __init__(self, scan_idx, rt, mz, intensity):
        """
        Function to initiate an ROI by providing the scan indices, 
        retention time, m/z and intensity.

        Parameters
        ----------------------------------------------------------
        scan_idx: int
            Scan index of the first ion in the ROI
        rt: float
            Retention time of the first ion in the ROI
        mz: float
            m/z value of the first ion in the ROI
        intensity: int
            Intensity of the first ion in the ROI
        """

        self.id = None
        self.scan_idx_seq = np.array([scan_idx], dtype = np.int32)

        self.rt_seq = np.array([rt], dtype = np.float64)
        self.mz_seq = np.array([mz], dtype = np.float64)
        self.int_seq = np.array([intensity], dtype = np.int64)
        self.ms2_seq = []

        # Count the gaps in the ROI's tail
        self.gap_counter = 0

        # Create attribute for the mean values of the ROI
        self.mz = mz
        self.rt = np.nan
        self.scan_number = -1
        self.peak_area = np.nan
        self.peak_height = np.nan
        self.peak_height_by_ave = np.nan
        self.best_ms2 = None

        # Ceature attribute for roi evaluation
        self.quality = None
        self.isotope = {
            'isotope': False,
            'isotope_number': None,
            'isotope_element': None,
            'parent_roi_id': None,
            'child_roi_id': None,
        }


    def extend_roi(self, scan_idx, rt, mz, intensity):
        """
        Function to extend an ROI by providing the scan indices, 
        retention time, m/z and intensity.

        Parameters
        ----------------------------------------------------------
        scan_idx: int
            Scan index of the ion to be added to the ROI
        rt: float
            Retention time of the ion to be added to the ROI
        mz: float
            m/z value of the ion to be added to the ROI
        intensity: int
            Intensity of the ion to be added to the ROI
        """

        # Extend the ROI
        self.scan_idx_seq = np.append(self.scan_idx_seq, scan_idx)
        self.rt_seq = np.append(self.rt_seq, rt)
        self.mz_seq = np.append(self.mz_seq, mz)
        self.int_seq = np.append(self.int_seq, intensity)
    

    def show_roi_info(self):
        """
        Function to print the information of the ROI.
        """

        print(f"ROI: {self.mz:.4f} m/z, {self.rt:.2f} min, {self.peak_area:.2f} area, {self.peak_height:.2f} height")
        print(f"ROI start time: {self.rt_seq[0]:.2f} min, ROI end time: {self.rt_seq[-1]:.2f} min")

    
    def roi_mz_error(self):
        """
        Function to calculate the m/z error (standard deviation of m/z) of the ROI.
        """

        return np.nanstd(self.mz_seq)
    

    def roi_length(self):
        """
        Function to calculate the length of the ROI.
        """

        return len(self.scan_idx_seq)


    def find_roi_rt(self):
        """
        Function to find the retention time of the ROI.
        """
        
        self.rt = self.rt_seq[np.argmax(self.int_seq)]
        self.scan_number = self.scan_idx_seq[np.argmax(self.int_seq)]

    
    def find_roi_height(self):
        """
        Function to find the peak height of the ROI.
        """

        self.peak_height = np.max(self.int_seq)

    
    def find_roi_area(self):
        """
        Function to find the peak area of the ROI using trapzoidal rule.

        """
        
        self.peak_area = np.trapz(y=self.int_seq, x=self.rt_seq) * 60 # use seconds to calculate area
    

    def find_roi_height_by_ave(self):
        """
        Function to find the peak height of the ROI by averaging
        the heighest three intensities.
        """

        d = np.sort(self.int_seq)[-3:]
        # calculate mean of non-zero values
        d = d[d != 0]
        self.peak_height_by_ave = np.mean(d, dtype=np.int64)
    

    def sum_roi(self):
        """
        Function to summarize the ROI to generate attributes.
        """

        # count the number of zeros in the end of self.int_seq
        counter = 0
        for i in range(len(self.int_seq)-1, -1, -1):
            if self.int_seq[i] == 0:
                counter += 1
            else:
                break
        
        # keep one zero in the end of ROI
        if counter > 1:
            self.mz_seq = self.mz_seq[:(1-counter)]
            self.int_seq = self.int_seq[:(1-counter)]
            self.rt_seq = self.rt_seq[:(1-counter)]
            self.scan_idx_seq = self.scan_idx_seq[:(1-counter)]
        
        self.find_roi_rt()
        self.find_roi_height()
        self.find_roi_area()
        self.find_roi_height_by_ave()
        self.mz = np.nanmean(self.mz_seq)
    

    def subset_roi(self, start, end):
        """
        Function to subset the ROI by providing the positions.

        Parameters
        ----------------------------------------------------------
        start: int
            The start position of the ROI to be subsetted.
        end: int
            The end position of the ROI to be subsetted.
        """

        self.scan_idx_seq = self.scan_idx_seq[start:end]
        self.rt_seq = self.rt_seq[start:end]
        self.mz_seq = self.mz_seq[start:end]
        self.int_seq = self.int_seq[start:end]

        ms2_seq = []

        for ms2 in self.ms2_seq:
            if ms2.scan > self.scan_idx_seq[0] and ms2.scan < self.scan_idx_seq[-1]:
                ms2_seq.append(ms2)
        
        self.ms2_seq = ms2_seq


    def find_best_ms2(self):
        """
        Function to find the best MS2 spectrum of the ROI.
        """

        if len(self.ms2_seq) > 1:
            total_ints = [np.sum(ms2.prod_int_seq) for ms2 in self.ms2_seq]
            self.best_ms2 = self.ms2_seq[np.argmax(total_ints)]
        elif len(self.ms2_seq) == 1:
            self.best_ms2 = self.ms2_seq[0]