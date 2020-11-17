import copy
import time


def hike(fpath):
    # open the file and calls each function
    with open(fpath, 'r', encoding='utf-8') as f:
        global upper_hike_limits, upper_section_limits, lower_hike_limits, lower_section_limits
        data = f.readlines()
        data = list(map(str.strip, data))
        min_dist_s, max_dist_s, min_time_s, max_time_s, min_ele_s, max_ele_s = data[0].split(
        )
        upper_section_limits = [
            int(max_ele_s), int(max_dist_s), int(max_time_s)]
        lower_section_limits = [
            int(min_ele_s), int(min_dist_s), int(min_time_s)]
        min_dist_h, max_dist_h, min_ele_h, max_ele_h = data[1].strip().split()
        upper_hike_limits = [int(max_ele_h), int(max_dist_h)]
        lower_hike_limits = [int(min_ele_h), int(min_dist_h)]
        cp_data = list(map(str.split, data[3:]))
        cp_data = list(map(lambda X: (
            [int(X[0]), int(X[1]), int(X[2]), int(X[3])]), cp_data))
        new_camps = sortOutCampsites(cp_data)
        sections = makeSections(new_camps)
        # print(sections)
        best_hike = findBestHike(sections)
    return str(best_hike[0][2]) + ' ' + str(best_hike[0][1]) + ' ' + str(best_hike[0][0])


def sortOutCampsites(check_points_data):
    new_camps = []
    elevation = 0
    for checkpoint in check_points_data:
        if len(new_camps) != 0:
            # determine the uphill elevation difference
            if new_camps[-1][1] < checkpoint[1]:
                elevation += checkpoint[1] - new_camps[-1][1]
            new_camps[-1][1] = checkpoint[1]
        if checkpoint[0] == 1:
            # if this is a camp site, add the uphill elevation difference
            if len(new_camps) != 0:
                new_camps[-1][1] = elevation
            new_camps.append(checkpoint)
            # set elevation back to 0 when a section has been decided
            elevation = 0
        else:
            # add this cp to the last camp site
            if len(new_camps) != 0:
                new_camps[-1][2] += checkpoint[2]
                new_camps[-1][3] += checkpoint[3]
            else:
                pass
    # last section is always 000
    new_camps[-1] = [1, 0, 0, 0]
    return new_camps


def withinUpperSectionLimits(limits, section):
    return section[1] <= limits[0] and section[2] <= limits[1] and section[3] <= limits[2]


def withinLowerSectionLimits(limits, section):
    return section[1] >= limits[0] and section[2] >= limits[1] and section[3] >= limits[2]


def makeSections(campsites):
    sections = []
    right_end = 0  # right end of the window
    for left_end in range(len(campsites)):  # left end of the window
        if len(sections) == 0:
            # set section to nothing in the beginning
            currentSection = [0, 0, 0, 0]
        else:
            # set current section to the latest section
            currentSection = copy.deepcopy(sections[-1])
            currentSection[1] -= campsites[left_end - 1][1]
            currentSection[2] -= campsites[left_end - 1][2]
            currentSection[3] -= campsites[left_end - 1][3]
        if left_end == len(campsites) - 1:
            # if at the last camp append nothing because no section can start there
            sections.append([0, 0, 0, 0])
            break
        while withinUpperSectionLimits(upper_section_limits, currentSection) and right_end != len(campsites):
            currentSection[1] += campsites[right_end][1]
            currentSection[2] += campsites[right_end][2]
            currentSection[3] += campsites[right_end][3]
            right_end += 1
        # move one section back because the loops quits only after the limit is exceeded
        right_end -= 1
        currentSection[1] -= campsites[right_end][1]
        currentSection[2] -= campsites[right_end][2]
        currentSection[3] -= campsites[right_end][3]
        currentSection[0] = right_end - left_end
        if withinLowerSectionLimits(lower_section_limits, currentSection):
            sections.append(currentSection)
        else:
            sections.append([0, 0, 0, 0])
            # if there is no section starting at this cp then i set s back to the value of i
            right_end = copy.deepcopy(left_end)
    return sections


def withinUpperHikeLimits(limits, hike):
    return hike[1] <= limits[0] and hike[2] <= limits[1]


def withinLowerHikeLimits(limits, hike):
    return hike[1] >= limits[0] and hike[2] >= limits[1]


def betterHike(hike1, hike2):
    if hike1[2] > hike2[2]:
        return True
    elif hike1[2] == hike2[2]:
        if hike1[1] > hike2[1]:
            return True
        elif hike1[1] == hike2[1]:
            if hike1[0] < hike2[0]:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def findBestHike(sections):
    # starts a hike at each camp where a section starts and then compares them
    hikes = [[0, 0, 0]]
    for i in range(len(sections)):
        if sections[i][0] != 0:
            currentHike = [0, 0, 0]
            j = 0
            while i + j < len(sections):
                if sections[i + j][0] == 0:
                    break
                currentHike[0] += 1
                currentHike[1] += sections[i + j][1]
                currentHike[2] += sections[i + j][2]
                if not withinUpperHikeLimits(upper_hike_limits, currentHike):
                    # if limit has been exceeded then quit the loop
                    currentHike[0] -= 1
                    currentHike[1] -= sections[i + j][1]
                    currentHike[2] -= sections[i + j][2]
                    break
                j += sections[i + j][0]
            if withinLowerHikeLimits(lower_hike_limits, currentHike):
                if betterHike(currentHike, hikes[0]):
                    hikes[0] = currentHike
    return hikes


for i in range(1, 10):
    input_file = '/Users/tejas/Desktop/semester 2/hike data /pub' + \
        '0' + str(i) + '.in'
    t1 = time.time()
    output_prog = hike(input_file)
    t2 = time.time()
    ouput_file = '/Users/tejas/Desktop/semester 2/hike data /pub' + \
        '0' + str(i) + '.out'
    with open(ouput_file, 'r', encoding='utf-8') as out:
        output = out.readlines()
        output = output[0].strip()
    if output_prog == output:
        print('correct', output_prog, '|', output, 'time taken', t2-t1)
    else:
        print('wrong', output_prog, '|', output, 'time taken', t2 - t1)
t1 = time.time()
output_prog = hike('/Users/tejas/Desktop/semester 2/hike data /pub10.in')
t2 = time.time()
with open('/Users/tejas/Desktop/semester 2/hike data /pub10.out', 'r', encoding='utf-8') as out:
    output = out.readlines()
    output = output[0].strip()
print(output == output_prog, output_prog, '|', output, 'time taken', t2-t1)
