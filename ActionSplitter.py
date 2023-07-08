import bpy
import time

# set split frame numbers here
frame_splits = [100,250,384]

# set your wanted base name
base_name = "new_action"

action = bpy.context.object.animation_data.action
sorted_fcurves_info = []

for fcurve in action.fcurves:
    keyframe_points = list(fcurve.keyframe_points)
    keyframe_points.sort(key=lambda point: point.co.x)
    fcurve_info = {
        "data_path": fcurve.data_path,
        "array_index": fcurve.array_index,
        "keyframe_points": keyframe_points
    }
    sorted_fcurves_info.append(fcurve_info)

offset = 0

for i, frame_split in enumerate(frame_splits):

    #Create new action
    new_action = bpy.data.actions.new(name=f"{base_name}_{i+1}")
    print(f"{new_action.name}")
	
    #Copy key_points
    for j, fcurve_info in enumerate(sorted_fcurves_info):
        print(f"copying {i},{j}: {time.perf_counter()}")
        new_fcurve = new_action.fcurves.new(data_path=fcurve_info["data_path"], index=fcurve_info["array_index"])
        for keyframe_point in fcurve_info["keyframe_points"]:
            if keyframe_point.co.x >= frame_split:
                break
            new_point = new_fcurve.keyframe_points.insert(frame=int(keyframe_point.co.x) - offset, value=keyframe_point.co.y) #Simply set value to the new one, some infos may be missed.
	    #new_point.xxx = keyframe_point.xxx

    print(f"copy finished {i}: {time.perf_counter()}")
	
    for j,fcurve_info in enumerate(sorted_fcurves_info):
        print(f"removing {i},{j}: {time.perf_counter()}")
	fcurve_info["keyframe_points"] = [p for p in fcurve_info["keyframe_points"] if p.co.x >= frame_split]
			
    print(f"remove finished {i}: {time.perf_counter()}")
    offset = frame_split
	
print(f"Finished!")
