from dn_photophys_analysis.file_io import load_image, save_localisation_table
from dn_photophys_analysis.image_analysis import get_spots, get_spots_denoised
from dn_photophys_analysis.single_mol_fitting import localise_frame
import argparse
import os
import time

def check_args(args: object):

    arg_dict = vars(args)

    for arg in arg_dict:
        if not arg:
            raise TypeError("One or more required arguments are missing.")
    
    if not os.path.isdir(arg_dict["image_path"]):
        raise FileNotFoundError("Input image does not exist")

    if not os.path.isdir(arg_dict["output_path"]):
        raise FileNotFoundError("Output folder does not exist")

    if not os.path.isdir(arg_dict["dn_image_path"]):
        raise FileNotFoundError("Denoised image does not exist.")
    
    if arg_dict["pixel_size_um"] <= 0:
        raise ValueError("Pixel size cannot be zero or below.")
    
    if arg_dict["adu"] <= 0:
        raise ValueError("ADU cannot be zero or below.")
    
    if arg_dict["gain"] < 1:
        raise ValueError("Gain cannot be below 1.")
    
    if arg_dict["offset"] <= 0:
        raise ValueError("Offset cannot be zero or below")

def main():

    parser = argparse.ArgumentParser()

    parser.add_argument("--image_path", type=str)
    parser.add_argument("--dn_image_path", type=str)
    parser.add_argument("--output_path", type=str)
    parser.add_argument("--pixel_size_um", type=float)
    parser.add_argument("--adu", type=float)
    parser.add_argument("--gain", type=int)
    parser.add_argument("--offset", type=float)

    opt = parser.parse_args()
    check_args(opt)

    # SPECS #

    frame_num, id = 1, 1

    localisations = []
    dn_localisations = []

    im_stack = load_image(opt.image_path)
    dn_stack = load_image(opt.dn_image_path)

    start = time.time()

    for i in range(0, im_stack.shape[0]):

        frame = im_stack[i]
        dn_frame = dn_stack[i]

        image_spots, maxima_coords = get_spots(frame, opt.pixel_size_um)
        dn_image_spots, dn_maxima_coords = get_spots_denoised(dn_frame, frame, 
                                                              opt.pixel_size_um)

        frame_locs = localise_frame(image_spots,
                                    maxima_coords,
                                    pix_res=opt.pixel_size_um,
                                    frame_num=frame_num,
                                    id_num=id,
                                    adu=opt.adu,
                                    gain=opt.gain,
                                    offset=opt.offset)
        
        dn_frame_locs = localise_frame(dn_image_spots,
                                    dn_maxima_coords,
                                    pix_res=opt.pixel_size_um,
                                    frame_num=frame_num,
                                    id_num=id,
                                    adu=opt.adu,
                                    gain=opt.gain,
                                    offset=opt.offset)
        
        localisations.append(frame_locs)
        dn_localisations.append(dn_frame_locs)

        id += frame_locs.shape[0]
        frame_num += 1

        if frame_num % 100 == 0:

            print(
                "Processed " + str(frame_num) + "/" + str(im_stack.shape[0]) + " frames"
            )
    
    end = time.time()
    print(str(end - start) + ' seconds.')
    
    save_localisation_table(localisations, opt.output_path)
    save_localisation_table(dn_localisations, opt.output_path, denoised='y')

if __name__ == "__main__":

    main()
