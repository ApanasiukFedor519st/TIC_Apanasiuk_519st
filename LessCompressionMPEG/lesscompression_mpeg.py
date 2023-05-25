import math
import os
import random
import cv2
import numpy as np
from matplotlib import pyplot as plt


def videoFrames(filename, first_frame, second_frame):
    cap = cv2.VideoCapture(filename)
    cap.set(cv2.CAP_PROP_POS_FRAMES, first_frame - 1)
    success1, frame1 = cap.read()
    cap.set(cv2.CAP_PROP_POS_FRAMES, second_frame - 1)
    success2, frame2 = cap.read()
    cap.release()
    return frame1, frame2


def bitsPerPixel(image):
    height, width = image.shape
    image_list = image.tolist()
    bits = 0
    for row in image_list:
        for pixel in row:
            bits += math.log2(abs(pixel) + 1)
    return bits / (height * width)


def reconstructTarget(residual, predicted):
    return np.add(residual, predicted)


def residual(target, predicted):
    return np.subtract(target, predicted)


def searchBlockBody(anchor, target, block_size, search_area=7):
    height, width = anchor.shape
    h_segments, w_segments = segmentImage(anchor, block_size)
    predicted = np.ones((height, width)) * 255
    block_count = 0
    for y in range(0, int(h_segments * block_size), block_size):
        for x in range(0, int(w_segments * block_size), block_size):
            block_count += 1
            target_block = target[y:y + block_size, x:x + block_size]
            anchor_search_area = anchorSearchArea(x, y, anchor, block_size, search_area)
            anchor_block = getBestMatch(target_block, anchor_search_area, block_size)
            predicted[y:y + block_size, x:x + block_size] = anchor_block
    assert block_count == int(h_segments * w_segments)
    return predicted


def segmentImage(anchor, block_size=16):
    height, width = anchor.shape
    h_segments = int(height / block_size)
    w_segments = int(width / block_size)
    return h_segments, w_segments


def anchorSearchArea(x, y, anchor, block_size, search_area):
    height, width = anchor.shape
    center_x, center_y = getCenter(x, y, block_size)
    start_x = max(0, center_x - int(block_size / 2) - search_area)
    start_y = max(0, center_y - int(block_size / 2) - search_area)
    anchor_search = anchor[start_y:min(start_y + search_area * 2 + block_size, height),
                           start_x:min(start_x + search_area * 2 + block_size, width)]
    return anchor_search


def getCenter(x, y, block_size):
    center_x = x + int(block_size / 2)
    center_y = y + int(block_size / 2)
    return center_x, center_y


def getBestMatch(target_block, anchor_search_area, block_size):
    step = 4
    ah, aw = anchor_search_area.shape
    acy, acx = int(ah / 2), int(aw / 2)
    min_mad = float("+inf")
    min_p = None
    while step >= 1:
        p1 = (acx, acy)
        p2 = (acx + step, acy)
        p3 = (acx, acy + step)
        p4 = (acx + step, acy + step)
        p5 = (acx - step, acy)
        p6 = (acx, acy - step)
        p7 = (acx - step, acy - step)
        p8 = (acx + step, acy - step)
        p9 = (acx - step, acy + step)
        point_list = [p1, p2, p3, p4, p5, p6, p7, p8, p9]
        for p in range(len(point_list)):
            a_block = getBlockZone(point_list[p], anchor_search_area, target_block, block_size)
            mad = getMAD(target_block, a_block)
            if mad < min_mad:
                min_mad = mad
                min_p = point_list[p]
        step = int(step / 2)
    px, py = min_p
    px, py = px - int(block_size / 2), py - int(block_size / 2)
    px, py = max(0, px), max(0, py)
    match_block = anchor_search_area[py:py + block_size, px:px + block_size]
    return match_block


def getBlockZone(p, anchor_search_area, target_block, block_size):
    px, py = p
    px, py = px - int(block_size / 2), py - int(block_size / 2)
    px, py = max(0, px), max(0, py)
    a_block = anchor_search_area[py:py + block_size, px:px + block_size]
    try:
        assert a_block.shape == target_block.shape
    except Exception as e:
        print(e)
    return a_block


def getMAD(target_block, anchor_block):
    return np.sum(np.abs(np.subtract(target_block, anchor_block))) / (target_block.shape[0] * target_block.shape[1])


def main(anchor_frame, target_frame, block_size, save_output=True):
    bits_anchor = []
    bits_diff = []
    bits_predicted = []
    height, width, channels = anchor_frame.shape
    print(height, width, channels)
    diff_frame_rgb = np.zeros((height, width, channels))
    predicted_frame_rgb = np.zeros((height, width, channels))
    residual_frame_rgb = np.zeros((height, width, channels))
    restore_frame_rgb = np.zeros((height, width, channels))
    for i in range(channels):
        anchor_frame_c = anchor_frame[:, :, i]
        target_frame_c = target_frame[:, :, i]
        diff_frame = cv2.absdiff(anchor_frame_c, target_frame_c)
        predicted_frame = searchBlockBody(anchor_frame_c, target_frame_c, block_size)
        residual_frame = residual(target_frame_c, predicted_frame)
        reconstruct_target_frame = reconstructTarget(residual_frame, predicted_frame)
        bits_anchor += [bitsPerPixel(anchor_frame_c)]
        bits_diff += [bitsPerPixel(diff_frame)]
        bits_predicted += [bitsPerPixel(residual_frame)]
        diff_frame_rgb[:, :, i] = diff_frame
        predicted_frame_rgb[:, :, i] = predicted_frame
        residual_frame_rgb[:, :, i] = residual_frame
        restore_frame_rgb[:, :, i] = reconstruct_target_frame
    output_dir = "Results"
    is_dir = os.path.isdir(output_dir)
    if not is_dir:
        os.mkdir(output_dir)
    if save_output:
        cv2.imwrite(f"{output_dir}/First_frame.png", anchor_frame)
        cv2.imwrite(f"{output_dir}/Second_frame.png", target_frame)
        cv2.imwrite(f"{output_dir}/Difference_between_frames.png", diff_frame_rgb)
        cv2.imwrite(f"{output_dir}/Prediction_frame.png", predicted_frame_rgb)
        cv2.imwrite(f"{output_dir}/Residual_frame.png", residual_frame_rgb)
        cv2.imwrite(f"{output_dir}/Restore_frame.png", restore_frame_rgb)
        bar_width = 0.25
        fig = plt.subplots(figsize=(12, 8))
        p1 = [sum(bits_anchor), bits_anchor[0], bits_anchor[1], bits_anchor[2]]
        diff = [sum(bits_diff), bits_diff[0], bits_diff[1], bits_diff[2]]
        mpeg = [sum(bits_predicted), bits_predicted[0], bits_predicted[1], bits_predicted[2]]
        br1 = np.arange(len(p1))
        br2 = [x + bar_width for x in br1]
        br3 = [x + bar_width for x in br2]
        br4 = [x + bar_width for x in br3]
        plt.bar(br1, p1, color='r', width=bar_width, edgecolor='grey', label='Bit per pixel for anchor frame')
        plt.bar(br2, diff, color='g', width=bar_width, edgecolor='grey', label='Bit per pixel for difference frame')
        plt.bar(br3, mpeg, color='b', width=bar_width, edgecolor='grey', label='Bit per pixel for motion-compensated difference')
        plt.title(f'Compression ratio = {round(sum(bits_anchor) / sum(bits_predicted), 2)}', fontweight='bold', fontsize=15)
        plt.ylabel('Bit per pixel', fontweight='bold', fontsize=15)
        plt.xticks([r + bar_width for r in range(len(p1))],
                   ['Bit/Pixel RGB', 'Bit/Pixel R', 'Bit/Pixel G', 'Bit/Pixel B'])
        plt.legend()
        plt.savefig(f'{output_dir}/Histogram_bit_per_pixel_for_different_encodings.png', dpi=600)


if __name__ == "__main__":
    random_frame = random.randint(0, 3000)
    frame1, frame2 = videoFrames('sample4.avi', random_frame, random_frame + 1)
    main(frame1, frame2, 32, save_output=True)
