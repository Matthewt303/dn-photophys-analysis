import numpy as np
import pandas as pd
import tifffile as tiff
import os

def load_image(path: str):

    with tiff.TiffFile(path) as tif:
        memmap_stack = tif.asarray(out='memmap')
    
    return memmap_stack.astype(np.float32)

def save_localisation_table(loc_data: list, out_folder: str,
                            denoised=None):

    localisation_data = np.vstack(loc_data).reshape(-1, 8)

    # Remove unrealistically large uncertainties.
    localisation_data = localisation_data[localisation_data[:, -1] < 500]

    headers = ['id',
               'frame',
               'x [nm]',
               'y [nm]',
               'sigma [nm]',
               'intensity [photon]',
               'offset [photon]',
               #'bkgstd [photon]',
               'uncertainty [nm]']
    
    dataframe = pd.DataFrame(data=localisation_data,
                             columns=headers,
                             dtype=np.float32)
    
    df_filt = dataframe[dataframe['uncertainty [nm]'].notnull()]

    if denoised is not None:

        df_filt.to_csv(os.path.join(out_folder, 'dn_reconstruction_tstorm.csv'),
                     sep=',',
                     index=False)
    
    else:
    
        df_filt.to_csv(os.path.join(out_folder, 'reconstruction_tstorm.csv'),
                     sep=',',
                     index=False)

def collate_locs_paths(folder: str) -> list[str]:

    file_paths = os.listdir(folder)

    loc_paths = [
        os.path.join(folder, path) for path in file_paths
        if path.endswith('.csv')
    ]

    return sorted(loc_paths)

def load_loc_table(path): 

    data = pd.read_csv(path, sep=',', header=None,
                       engine='pyarrow', skiprows=1)
    
    return np.array(data).astype(np.float32)

def load_locs_frames_intensities(path):

    data = pd.read_csv(path, sep=',', header=None, engine='pyarrow',
    usecols=[1, 5], skiprows=1)

    return np.array(data).astype(np.float32)

def load_locs_inten_bg_lp(path: str):

    """
    Loads intensity, offset, and localisation precision from loc table.
    ----------------------------------------
    In:
    path - file path for loc table.
    ----------------------------------------
    Out:
    n x 3 numpy array, where each col is a photophysical param.
    """

    data = pd.read_csv(path, sep=",", header=None, engine="pyarrow",
                       skiprows=1)
    
    return np.array(data).astype(np.float32)

def save_p_val(p_val: float, relation: str, param_name: str, out: str):

    with open(os.path.join(out, param_name + "_pval.txt"), "w") as f:

        if relation == "paired":

            f.write("The p-value for the Wilcoxon signed rank test is " \
            + "{:10.4f}".format(p_val))

        elif relation == "independent":

            f.write("The p-value for the Kruskal-Wallis test is "
                    + "{:10.4f}".format(p_val))

def save_all_results(
    data_A: "np.ndarray",
    data_B: "np.ndarray",
    data_A_loc_files: list[str],
    data_B_loc_files: list[str],
    cond_a: str,
    cond_b: str,
    output_folder: str,
) -> "pd.DataFrame":
    """
    This function converts the FRC results into a pandas dataframe where the columns
    are: file name, designation, and the FRC resolution. The dataframe is saved in the
    output folder as a .csv file.
    -----------------------
    IN:
    raw_frc - FRC resolutions from the noisy dataset
    denoised_frc - FRC resolutions from the denoised dataset.
    raw_loc_files - list of files for the noisy data
    denoised_loc_files - list of files for the denoised data.
    cond_a - the designation for the control.
    cond_b - the designation for the test data.
    output_folder - where the dataframe will be saved
    ----------------------
    OUT:
    dataframe - pandas dataframe with the files, condition, and FRC resolutions.
    ----------------------
    """
    designate_raw, designate_denoised = (
        [cond_a] * len(data_A_loc_files),
        [cond_b] * len(data_B_loc_files),
    )

    designations = designate_raw + designate_denoised

    all_results = np.vstack((data_A, data_B))

    cols = [
            "Intensity (photons)",
            "Background (photons)",
            "Localisation precision (nm)"
            ]

    dataframe = pd.DataFrame(all_results, columns=cols)

    dataframe.insert(0, "Designation", designations)

    dataframe.to_csv(os.path.join(output_folder, "all_results.csv"), index=False)

    return dataframe