import os, json

###################################
"""
Edit here. COLOR will be replaced with an item of each 16 colors.
white colored block models will not be made, as it will be treated
as the base the other colors will parent from.
"""
namespace = "another_furniture"
generate_pre = [
    {"name": "WOODTYPE_chair", "wood_types": True, "blockstate_preset": "4_way", "tags": [f"{namespace}:blocks/chairs", {"minecraft:blocks/mineable/axe": f"{namespace}:blocks/chairs"}, {"minecraft:blocks/unstable_bottom_center": f"{namespace}:blocks/chairs"}], "recipe": {"type":"minecraft:crafting_shaped","pattern":["# ","##","//"],"key":{"#":{"item":"minecraft:WOODTYPE_planks"},"/":{"item":"minecraft:stick"}},"result":{"item":"another_furniture:WOODTYPE_chair","count":1},"group":"chairs"}},
    {"name": "WOODTYPE_shelf", "wood_types": True, "blockstate_preset": "shelf", "tags": [f"{namespace}:blocks/shelves", {"minecraft:blocks/mineable/axe": f"{namespace}:blocks/shelves"}], "recipe": {"type":"minecraft:crafting_shaped","pattern":["###","/  "],"key":{"#":{"item":"minecraft:WOODTYPE_planks"},"/":{"item":"minecraft:stick"}},"result":{"item":"another_furniture:WOODTYPE_shelf","count":1},"group":"shelves"}},
    {"name": "WOODTYPE_table", "wood_types": True, "blockstate_preset": "table", "tags": [f"{namespace}:blocks/tables", {"minecraft:blocks/mineable/axe": f"{namespace}:blocks/tables"}], "recipe": {"type":"minecraft:crafting_shaped","pattern":["###","/ /"],"key":{"#":{"item":"minecraft:WOODTYPE_planks"},"/":{"item":"minecraft:stick"}},"result":{"item":"another_furniture:WOODTYPE_table","count":1},"group":"tables"}},
    {"name": "COLOR_stool", "colored": True, "tags": [f"{namespace}:blocks/stools", {"minecraft:blocks/mineable/axe": f"{namespace}:blocks/stools"}, {"minecraft:blocks/unstable_bottom_center": f"{namespace}:blocks/stools"}], "recipe": {"type":"minecraft:crafting_shaped","pattern":["#W#","/ /"],"key":{"#":{"tag":"minecraft:planks"},"W":{"item":"minecraft:COLOR_wool"},"/":{"item":"minecraft:stick"}},"result":{"item":"another_furniture:COLOR_stool","count":1},"group":"stools"}},
    {"name": "service_bell"}
]


def class_names(item_name):
    class_type = "CLASS"
    if item_name.endswith("chair"):
        class_type = "ChairBlock"
    elif item_name.endswith("shelf"):
        class_type = "ShelfBlock"
    elif item_name.endswith("stool"):
        class_type = "StoolBlock"
    elif item_name.endswith("table"):
        class_type = "TableBlock"
    return class_type

def material_names(item_name):
    material_type = "WOOD"
    for wood_type in wood_types:
        if wood_type.split(":")[1] in item_name:
            material_type = "WOOD"
            for non_flammable_wood in non_flammable_woods:
                if non_flammable_wood in item_name:
                    return "NETHER_WOOD"
                
    if item_name.endswith("stool"):
        material_type = "WOOD"
    return material_type

###################################
colors = [
    "white", "orange", "magenta", "light_blue", "yellow", "lime", "pink", "gray",
    "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"
]

wood_types = [
    "minecraft:oak", "minecraft:spruce", "minecraft:birch", "minecraft:jungle", "minecraft:acacia",
    "minecraft:dark_oak", "minecraft:crimson", "minecraft:warped", "quark:azalea", "quark:blossom",
    "ecologics:azalea", "ecologics:coconut", "ecologics:walnut"
]

non_flammable_woods = [
    "crimson", "warped"
]

def make_file_if_not_exist(path, json_dict):
    if not os.path.exists(path):
        with open(path, "w+") as f:
            f.write(json.dumps(json_dict, indent=4) + "\n")


current_dir = os.getcwd()
block_loot_tables_pre = f"{current_dir}\\src\\main\\resources\\data\\{namespace}\\loot_tables\\blocks"
recipes_pre = f"{current_dir}\\src\\main\\resources\\data\\{namespace}\\recipes"
block_model_pre = f"{current_dir}\\src\\main\\resources\\assets\\{namespace}\\models\\block"
item_model_pre = f"{current_dir}\\src\\main\\resources\\assets\\{namespace}\\models\\item"
blockstates_pre = f"{current_dir}\\src\\main\\resources\\assets\\{namespace}\\blockstates"
langs = f"{current_dir}\\src\\main\\resources\\assets\\{namespace}\\lang\\en_us.json"

def generate_list(generate_pre):
    generate = []
    for item in generate_pre:
        item2 = {**{"colored": False, "wood_types": False, "made_from_block_namespace": "minecraft", "blockstate_preset": "normal", "tags": [], "recipe": {}}, **item}
        item_name1 = item2["name"]
        if "colored" in item2 and item2["colored"]:
            for color in colors:
                dct = {**item2, **{"name": item_name1.replace("COLOR", color)}, **{"color": color}}
                generate.append(dct)
                
        elif "wood_types" in item2 and item2["wood_types"]:
            for wood_type in wood_types:
                wood_type_namespace = wood_type.split(":")[0]
                wood_type_no_namespace = wood_type.split(":")[1]
                dct = {**item2, **{"name": item_name1.replace("WOODTYPE", wood_type_no_namespace)}, **{"made_from_block_namespace": wood_type_namespace}, **{"wood_type": wood_type_no_namespace}}
                generate.append(dct)
                
        else:
            dct = {**item2, **{"name": item_name1}}
            generate.append(dct)
        item2 = {}
    return generate


tags_dict = {}

def generate_all(generate):
    lang = {}
    namespaced_items = []
    for item in generate:
            
        item_name = item["name"]
        type_of_item = item_name.split("_")[-1]

        made_from_block_namepath = ""
        if item['made_from_block_namespace'] != "minecraft":
            made_from_block_namepath = item['made_from_block_namespace'] + "_"

        namespaced_item = namespace + ":" + made_from_block_namepath + item_name

        
        #########################
        #Block Loot Tables
        
        make_file_if_not_exist(f"{block_loot_tables_pre}\\{made_from_block_namepath}{item_name}.json",
            {"type":"minecraft:block","pools":[{"rolls":1,"entries":[{"type":"minecraft:item","name":namespaced_item}],"conditions":[{"condition":"minecraft:survives_explosion"}]}]}
        )
        #########################
        # Block Models
        
        if type_of_item in ["stool"]:
            make_file_if_not_exist(f"{block_model_pre}\\{type_of_item}\\{item['color']}.json",
                {"parent":f"{namespace}:block/template/{type_of_item}","textures":{"all":f"{namespace}:block/{type_of_item}/{item['color']}","particle":f"minecraft:block/{item['color']}_wool"}}
            )
        elif item["wood_types"]:
            if item["blockstate_preset"] == "table":
                make_file_if_not_exist(f"{block_model_pre}\\table\\{made_from_block_namepath}{item['wood_type']}_leg.json",
                    {"parent": f"{namespace}:block/template/table_leg","textures":{"all":f"{namespace}:block/table/{made_from_block_namepath}{item['wood_type']}","particle":f"{item['made_from_block_namespace']}:block/{item['wood_type']}_planks"}}
                )
                make_file_if_not_exist(f"{block_model_pre}\\table\\{made_from_block_namepath}{item['wood_type']}_top.json",
                    {"parent": f"{namespace}:block/template/table_top","textures":{"all":f"{namespace}:block/table/{made_from_block_namepath}{item['wood_type']}","particle":f"{item['made_from_block_namespace']}:block/{item['wood_type']}_planks"}}
                )
            elif item["blockstate_preset"] == "shelf":
                make_file_if_not_exist(f"{block_model_pre}\\shelf\\{made_from_block_namepath}{item['wood_type']}_top.json",
                    {"parent": f"{namespace}:block/template/shelf_top","textures":{"all":f"{namespace}:block/shelf/{made_from_block_namepath}{item['wood_type']}","particle":f"{item['made_from_block_namespace']}:block/{item['wood_type']}_planks"}}
                )
                make_file_if_not_exist(f"{block_model_pre}\\shelf\\{made_from_block_namepath}{item['wood_type']}_l.json",
                    {"parent": f"{namespace}:block/template/shelf_l","textures": {"all": f"{namespace}:block/shelf/{made_from_block_namepath}{item['wood_type']}","particle":f"{item['made_from_block_namespace']}:block/{item['wood_type']}_planks"}}
                )
                make_file_if_not_exist(f"{block_model_pre}\\shelf\\{made_from_block_namepath}{item['wood_type']}_r.json",
                    {"parent": f"{namespace}:block/template/shelf_r","textures": {"all": f"{namespace}:block/shelf/{made_from_block_namepath}{item['wood_type']}","particle":f"{item['made_from_block_namespace']}:block/{item['wood_type']}_planks"}}
                )
            elif type_of_item == "chair":
                make_file_if_not_exist(f"{block_model_pre}\\chair\\{made_from_block_namepath}{item['wood_type']}.json",
                    {"parent": f"{namespace}:block/template/chair","textures": {"all": f"{namespace}:block/chair/{made_from_block_namepath}{item['wood_type']}","particle":f"{item['made_from_block_namespace']}:block/{item['wood_type']}_planks"}}
                )
            else:
                make_file_if_not_exist(f"{block_model_pre}\\{item_name}.json",
                    {"parent": f"{namespace}:block/template/{type_of_item}","textures":{"all":f"{namespace}:block/{type_of_item}/{made_from_block_namepath}{item['wood_type']}","particle": f"{item['made_from_block_namespace']}:block/{item['wood_type']}_planks"}}
                )
        else:
            make_file_if_not_exist(f"{block_model_pre}\\{item_name}.json",
                {"parent":f"{namespace}:block/template/{item_name}","textures":{"all":f"{namespace}:block/{item_name}"}}
            )
        #########################
        #Item Models
        if type_of_item in ["table", "shelf"]:
            make_file_if_not_exist(f"{item_model_pre}\\{made_from_block_namepath}{item_name}.json",
                {"parent": f"{namespace}:block/template/{type_of_item}_full", "textures": {"all": f"{namespace}:block/{type_of_item}/{made_from_block_namepath}{item['wood_type']}"}}
            )
        elif type_of_item in ["chair"]:
            make_file_if_not_exist(f"{item_model_pre}\\{made_from_block_namepath}{item_name}.json",
                {"parent": f"{namespace}:block/{type_of_item}/{made_from_block_namepath}{item['wood_type']}"}
            )
        elif type_of_item in ["stool"]:
            make_file_if_not_exist(f"{item_model_pre}\\{made_from_block_namepath}{item_name}.json",
                {"parent": f"{namespace}:block/{type_of_item}/{item['color']}"}
            )
        else:
            make_file_if_not_exist(f"{item_model_pre}\\{made_from_block_namepath}{item_name}.json",
                {"parent": f"{namespace}:block/{item_name}"}
            )
        #########################
        #Blockstates
        
        if item["blockstate_preset"] == "normal":
            if type_of_item in ["stool"]:
                blockstate = {"variants": {"": {"model": f"{namespace}:block/{type_of_item}/{item['color']}"}}}
            else:
                blockstate = {"variants": {"": {"model": f"{namespace}:block/{made_from_block_namepath}{item_name}"}}}
        elif item["blockstate_preset"] == "4_way":
            blockstate_model_1 = f"{namespace}:block/{type_of_item}/{made_from_block_namepath}{item['wood_type']}"
            blockstate = {"variants": {"facing=north": {"model": blockstate_model_1},"facing=east": {"model": blockstate_model_1,"y": 90},"facing=south": {"model": blockstate_model_1,"y": 180},"facing=west": {"model": blockstate_model_1,"y": 270}}}
        elif item["blockstate_preset"] == "shelf":
            blockstate_model_1 = f"{namespace}:block/shelf/{made_from_block_namepath}{item['wood_type']}_top"
            blockstate_model_2 = f"{namespace}:block/shelf/{made_from_block_namepath}{item['wood_type']}_l"
            blockstate_model_3 = f"{namespace}:block/shelf/{made_from_block_namepath}{item['wood_type']}_r"
            blockstate = {"multipart":[{"when":{"facing":"north"},"apply":{"model":blockstate_model_1}},{"when":{"facing":"east"},"apply":{"model":blockstate_model_1,"y":90}},{"when":{"facing":"south"},"apply":{"model":blockstate_model_1,"y":180}},{"when":{"facing":"west"},"apply":{"model":blockstate_model_1,"y":270}},{"when":{"facing":"north","type":"0|1"},"apply":{"model":blockstate_model_2}},{"when":{"facing":"east","type":"0|1"},"apply":{"model":blockstate_model_2,"y":90}},{"when":{"facing":"south","type":"0|1"},"apply":{"model":blockstate_model_2,"y":180}},{"when":{"facing":"west","type":"0|1"},"apply":{"model":blockstate_model_2,"y":270}},{"when":{"facing":"north","type":"0|3"},"apply":{"model":blockstate_model_3}},{"when":{"facing":"east","type":"0|3"},"apply":{"model":blockstate_model_3,"y":90}},{"when":{"facing":"south","type":"0|3"},"apply":{"model":blockstate_model_3,"y":180}},{"when":{"facing":"west","type":"0|3"},"apply":{"model":blockstate_model_3,"y":270}}]}
        elif item["blockstate_preset"] == "table":
            blockstate_model_1 = f"{namespace}:block/table/{made_from_block_namepath}{item['wood_type']}_top"
            blockstate_model_2 = f"{namespace}:block/table/{made_from_block_namepath}{item['wood_type']}_leg"
            blockstate = {"multipart":[{"when":{"facing":"north"},"apply":{"model":blockstate_model_1}},{"when":{"facing":"east"},"apply":{"model":blockstate_model_1,"y":90}},{"when":{"facing":"south"},"apply":{"model":blockstate_model_1,"y":180}},{"when":{"facing":"west"},"apply":{"model":blockstate_model_1,"y":270}},{"when":{"leg_1":"true"},"apply":{"model":blockstate_model_2,"uvlock":True}},{"when":{"leg_2":"true"},"apply":{"model":blockstate_model_2,"y":90,"uvlock":True}},{"when":{"leg_3":"true"},"apply":{"model":blockstate_model_2,"y":180,"uvlock":True}},{"when":{"leg_4":"true"},"apply":{"model":blockstate_model_2,"y":270,"uvlock":True}}]}
        make_file_if_not_exist(f"{blockstates_pre}\\{made_from_block_namepath}{item_name}.json", blockstate)
        


        #########################
        #Recipes

        if not len(item["recipe"]) == 0:
            if item["colored"]:
                key = "W"
                data = item["color"]
                extra = "wool"
                
            elif item["wood_types"]:
                key = "#"
                data = item["wood_type"]
                extra = "planks"
                
            recipe = item["recipe"]
            key_namespace = recipe["key"][key]["item"].split(":")[0]
            recipe["key"][key]["item"] = f"{item['made_from_block_namespace']}:{data}_{extra}"
            recipe["result"]["item"] = namespaced_item
            if item["made_from_block_namespace"] != "minecraft":
                recipe["conditions"] = [{"type":"forge:mod_loaded","modid":item['made_from_block_namespace']}]
            make_file_if_not_exist(f"{recipes_pre}\\{made_from_block_namepath}{item_name}.json", recipe)

        if item_name.endswith("stool"):
            if not item["color"] == "white":
                make_file_if_not_exist(f"{recipes_pre}\\{made_from_block_namepath}{item_name}_dyeing.json", {"type": "minecraft:crafting_shapeless","ingredients": [{"item": f"{namespace}:white_{type_of_item}"},{"item": f"minecraft:{item['color']}_dye"}],"result":{"item":namespaced_item,"count": 1},"group":"stools"})
        #####
        #Compat - Corail Woodcutter
        if item["wood_types"]:
            if item["made_from_block_namespace"] == "minecraft":
                make_file_if_not_exist(f"{recipes_pre}\\{made_from_block_namepath}{item_name}_from_plank_woodcutting.json",{"type":"corail_woodcutter:woodcutting","conditions":[{"type":"forge:mod_loaded","modid":"corail_woodcutter"}],"ingredient":{"item":f"minecraft:{item['wood_type']}_planks"},"result":namespaced_item,"count":1})
                make_file_if_not_exist(f"{recipes_pre}\\{made_from_block_namepath}{item_name}_from_log_woodcutting.json",{"type":"corail_woodcutter:woodcutting","conditions":[{"type":"forge:mod_loaded","modid":"corail_woodcutter"}],"ingredient":{"tag":f"minecraft:{item['wood_type']}_logs"},"result":namespaced_item,"count":4})
            else:
                make_file_if_not_exist(f"{recipes_pre}\\{made_from_block_namepath}{item_name}_from_plank_woodcutting.json",{"type":"corail_woodcutter:woodcutting","conditions":[{"type":"forge:mod_loaded","modid":"corail_woodcutter"},{"type":"forge:mod_loaded","modid":item['made_from_block_namespace']}],"ingredient":{"item":f"{item['made_from_block_namespace']}:{item['wood_type']}_planks"},"result":namespaced_item,"count":1})
                make_file_if_not_exist(f"{recipes_pre}\\{made_from_block_namepath}{item_name}_from_log_woodcutting.json",{"type":"corail_woodcutter:woodcutting","conditions":[{"type":"forge:mod_loaded","modid":"corail_woodcutter"},{"type":"forge:mod_loaded","modid":item['made_from_block_namespace']}],"ingredient":{"tag":f"{item['made_from_block_namespace']}:{item['wood_type']}_logs"},"result":namespaced_item,"count":4})



        #########################
        #Tags #1

        for tag in item["tags"]:
            if type(tag) == str:
                if not tag in tags_dict:
                    tags_dict[tag] = []
                tags_dict[tag].append(namespaced_item)
                
                if item["wood_types"] and (item["wood_type"] in non_flammable_woods):
                    if not "minecraft:blocks/non_flammable_wood" in tags_dict:
                        tags_dict["minecraft:blocks/non_flammable_wood"] = []
                    tags_dict["minecraft:blocks/non_flammable_wood"].append(namespaced_item)
            elif type(tag) == dict:
                dict_key = str(list(tag.keys())[0])
                dict_value = "#" + str(list(tag.values())[0]).replace("blocks/","")
                
                if not dict_key in tags_dict:
                    tags_dict[dict_key] = []
                    
                if not dict_value in tags_dict[dict_key]:
                    tags_dict[dict_key].append(dict_value)
        
        #########################
        #Code
        class_type = class_names(item_name)
        material_name = material_names(item_name)

        if item["made_from_block_namespace"] == "minecraft":
            print(f'public static final RegistryObject<Block> {made_from_block_namepath.upper()}{item_name.upper()} = RegistryUtil.createBlockAndItem("{item_name.lower()}", () -> new {class_type}(Block.Properties.of(Material.{material_name}).strength(2.0F, 3.0F).sound(SoundType.WOOD)));')
        else:
            print(f'public static final RegistryObject<Block> {made_from_block_namepath.upper()}{item_name.upper()} = RegistryUtil.createBlockAndItemCompat(CompatUtil.{item["made_from_block_namespace"].upper()}_ID, "{item_name.lower()}", () -> new {class_type}(Block.Properties.of(Material.{material_name}).strength(2.0F, 3.0F).sound(SoundType.WOOD)));')


        
        #########################
        #Lang
        lang[f"itemGroup.{namespace}"] = "Another Furniture Mod"
        lang[f"block.{namespace}.service_bell.use"] = "Bell chimes"
        lang[f"block.{namespace}.{made_from_block_namepath}{item_name}"] = item_name.replace("_", " ").title()
        #########################
        namespaced_items.append(namespaced_item)
        
    make_file_if_not_exist(langs, lang)

    #########################
    #Ids List
    #
    #for x in namespaced_items:
    #    print(f'"{x}",')
    

generate = generate_list(generate_pre)
generate_all(generate)

for x in wood_types:
    print(f"ModBlocks.{x.replace('minecraft:','').replace(':','_').upper()}_SHELF.get(),")

for x in wood_types:
    print(f"ItemBlockRenderTypes.setRenderLayer(ModBlocks.{x.replace('minecraft:','').replace(':','_').upper()}_CHAIR.get(), RenderType.cutout());")

#########################
#Tags #2

for tag in tags_dict:
    block_tags = f"{current_dir}\\src\\main\\resources\\data\\{tag.replace(':', '/tags/')}.json"
    make_file_if_not_exist(block_tags, {"replace": False, "values": tags_dict[tag]})




