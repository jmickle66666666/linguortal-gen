from sys import argv
from omg import *
from omg.mapedit import *
    
def make_linguortal(inwad1, inwad2, linedef1, linedef2):
    wad1 = MapEditor(inwad1)
    wad2 = MapEditor(inwad2)

    whichnode = find_node_for_line(wad1, linedef1, 0)
    whichnode_back = find_node_for_line(wad1, linedef1, 1)
    
    nodenum = whichnode[0]
    nodenum_back = whichnode_back[0]
        
    childnum = whichnode[1]
    childnum_back = whichnode_back[1]
    
    whichseg = whichnode[2]
    
    for node in wad1.nodes:
        if node.right_index < 32768:
            node.right_index += 1
        if node.left_index < 32768:
            node.left_index += 1

    wad1.nodes.insert(0, copy(wad1.nodes[nodenum]))
        
    if(wad1.nodes[nodenum + 1].right_index == childnum):
        wad1.nodes[nodenum + 1].left_index = 0
        whichchild = 0
    else:
        wad1.nodes[nodenum + 1].right_index = 0
        whichchild = 1
    
    wad1.nodes[0].left_index = childnum
    wad1.nodes[0].right_index = childnum
        
    l1_vert = wad1.vertexes[wad1.linedefs[linedef1].vx_b]
    l2_vert = wad2.vertexes[wad2.linedefs[linedef2].vx_a]
    
    x_diff = l2_vert.x - l1_vert.x
    y_diff = l2_vert.y - l1_vert.y
        
    vlen  = len(wad1.vertexes)
    v2len = len(wad2.vertexes)
    
    ilen  = len(wad1.sidedefs)
    slen  = len(wad1.sectors)
    sslen = len(wad1.ssectors)
    llen  = len(wad1.linedefs)
    seglen = len(wad1.segs)
    
    for vx in wad2.vertexes:
        x, y = vx.x, vx.y
        wad1.vertexes.append(Vertex(x, y))
        
    for vx in wad2.vertexes:
        x, y = vx.x, vx.y
        x -= x_diff
        y -= y_diff
        wad1.vertexes.append(Vertex(x, y))
        
    for node in wad2.nodes:
        node.x_start -= x_diff
        node.y_start -= y_diff
        node.right_bbox_top -= y_diff
        node.right_bbox_bottom -= y_diff
        node.left_bbox_top -= y_diff
        node.left_bbox_bottom -= y_diff
        node.right_bbox_left -= x_diff
        node.right_bbox_right -= x_diff
        node.left_bbox_left -= x_diff
        node.left_bbox_right -= x_diff
        
    for line in wad2.linedefs:
        z = copy(line)
        z.vx_a += vlen
        z.vx_b += vlen
        if z.front != -1: z.front += ilen
        if z.back != -1: z.back += ilen
        wad1.linedefs.append(z)
    for side in wad2.sidedefs:
        z = copy(side)
        z.sector += slen
        wad1.sidedefs.append(z)
    for sector in wad2.sectors:
        z = copy(sector)
        wad1.sectors.append(z)
    for ssector in wad2.ssectors:
        z = copy(ssector)
        z.seg_a += seglen
        wad1.ssectors.append(z)
    for seg in wad2.segs:
        z = copy(seg)
        z.vx_a += vlen + v2len
        z.vx_b += vlen + v2len
        z.line += llen
        wad1.segs.append(z)
    
    wad1.nodes[0].x_start = -1024
    wad1.nodes[0].y_start = 32767
    wad1.nodes[0].x_vector = 2048
    wad1.nodes[0].y_vector = 0
    
    if(whichchild == 0):
        wad1.nodes[0].left_bbox_top = wad1.nodes[0].right_bbox_top
        wad1.nodes[0].left_bbox_bottom = wad1.nodes[0].right_bbox_bottom
        wad1.nodes[0].left_bbox_left = wad1.nodes[0].right_bbox_left
        wad1.nodes[0].left_bbox_right = wad1.nodes[0].right_bbox_right
        
    wad1.nodes[0].right_bbox_top = 0
    wad1.nodes[0].right_bbox_bottom = 0
    wad1.nodes[0].right_bbox_left = 0
    wad1.nodes[0].right_bbox_right = 0
    
    wad1nodenum = len(wad1.nodes)
    wad2nodenum = len(wad2.nodes)
    totalnodes = wad1nodenum + wad2nodenum
    
    for node in wad2.nodes:
        if(node.right_index >= 32768):
            node.right_index += sslen
        if(node.left_index >= 32768):
            node.left_index += sslen
    
    for i in range(1,wad1nodenum):
        if(wad1.nodes[i].right_index < 32768):
            wad1.nodes[i].right_index += wad2nodenum
        if(wad1.nodes[i].left_index < 32768):
            wad1.nodes[i].left_index += wad2nodenum
    
    wad1.nodes[0].left_index = wad2nodenum-1
    
    fart = wad2.nodes + wad1.nodes
    wad1.nodes = fart
    
    return wad1.to_lumps()

def find_node_for_line(map, linedef, side):
    numnodes = len(map.nodes)
    for i in range(numnodes):
        for child in [map.nodes[i].right_index,map.nodes[i].left_index]:
            if(child >= 32768):
                ssnum = child - 32768
                numsegs = map.ssectors[ssnum].numsegs
                startseg = map.ssectors[ssnum].seg_a
                for j in range(startseg, startseg + numsegs):
                    if((map.segs[j].line == linedef) and (map.segs[j].side == side)):
                        return [i,child,j]    
    print "** couldn't find node for line {}! **".format(linedef)

def main(args):
    if (len(args) < 5):
        print "    Omgifol script: generate linguortals\n"
        print "    Usage:"
        print "    linguortal.exe input1.wad map input2.wad map linedef1 linedef2 output.wad\n"
        print "    Creates linguortal in input1.wad, on the specified map. The portal connects to the "
        print "    specified linedef in input2.wad, on the specified map. The resulting map is placed "
        print "    in the specified output wad (created if it doesn't exist), using the first map number. \n"
        print "    Example:"
        print "    linguortal.exe my_wad.wad MAP01 portal.wad MAP01 30 25 my_linguortal.wad"
    else: 
        print "Loading %s..." % args[0]
        inwad1 = WAD()
        inwad2 = WAD()
        outwad = WAD()
        inwad1.from_file(args[0])
        inwad2.from_file(args[2])
        
        linedef1 = args[4]
        linedef2 = args[5]
        
        map1 = args[1]
        map2 = args[3]
        outwad.maps[map1] = make_linguortal(inwad1.maps[map1], inwad2.maps[map2], int(linedef1), int(linedef2))
        
        print "Saving %s..." % args[6]
        outwad.to_file(args[6])

if __name__ == "__main__": main(argv[1:])