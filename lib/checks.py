import os

def checks(image_folder, projection_folder, projection_delimiter):
    # Check 1
    assert os.path.isdir(image_folder), "Image folder does not exist."
    assert os.path.isdir(projection_folder), "Projection folder does not exist."
    print("Check 1 OK")
    
    #Check 2
    total_projections = 0
    prj_list = os.listdir(projection_folder)
    target_list = {}
    for prj in prj_list:
        with open("{}/{}".format(projection_folder, prj), "r") as prj_file:
            for line in prj_file:
                total_projections += 1
                line = line.strip()
                target_id, X, Y = line.split(projection_delimiter,2)

                if target_id not in target_list.keys():
                    target_list[target_id] = [target_id, 1]
                    
                elif target_id in target_list.keys():
                    for k in target_list.keys():
                        if target_id == k:
                            target_list[k][1] +=  1
    print("Check 2 OK")
                            
    
    #print(target_list)
    print("Number of targets in the projection folder: {}".format(len(target_list)))
    print("Number of total projections: {}".format(total_projections))
    #print(len(prj_list))
    
    