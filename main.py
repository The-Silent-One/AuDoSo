from lxml import etree
from copy import deepcopy
import sys

def saveFile(root):
    with open("score.xml","w") as f:
        f.write(etree.tostring(root,pretty_print=True).decode())
    
def prettyPrint(root):
    #if variable is a list, do one layer reccursion
    if isinstance(root,list):
        for elt in root:
            prettyPrint(elt)
        return
    lines = etree.tostring(root,pretty_print=True).decode().split("\n")

    for l in lines:
        print(l)

#remove useless information from score
def simplifyScore(root):
    for elt in root:
        if elt.tag!="part" and elt.tag!="part-list":
            root.remove(elt)
#clean note tag
def cleanNote(note):
    #remove internal attribute
    note.attrib.pop("default-x", None)
    #list of tags to keep, staff is not essential
    keep = ["pitch","duration","type","chord"]#,"staff"]
    for elt in note:
        if elt.tag not in keep:
            note.remove(elt)
            
#clean atrributes tag
def cleanAttributes(attr):
    #list of tags to keep, clef is not essential
    keep = ["divisions","time","staves"]#,"clef"]
    for elt in attr:
        if elt.tag not in keep:
            attr.remove(elt)

#these functions clean nothing, created so the clean fucntion doesn't delete the elements automatically
def cleanMeasure(root):
    return
        
#clean each element depending on its type
def clean(root):
    #remove internal attribute
    root.attrib.pop("width", None)
    for elt in root:
        try:
            #call specific function depending on type
            #format : globals()[fucntionname](variables)
            globals()['clean'+elt.tag.upper()[0]+elt.tag[1:]](elt)
        except:
            #element doesn't have a function related to its type, hence removing it
            elt.getparent().remove(elt)

#return list of bool if a note contains chord tag
def containsChord(measure):
    return [len(elt.xpath("chord"))>0 for elt in measure]

#change empty pitch note to rests
def createRest(measure):
    for note in measure.xpath("note"):
        if not(note.xpath("pitch")):
            note.tag = "rest"

#remove pitch tag and make note 1 depth
def simplifyNote(measure):
    for note in measure.xpath("note"):
        note.insert(0,note.xpath("pitch/step")[0])
        note.insert(1,note.xpath("pitch/octave")[0])
        note.remove(note.xpath("pitch")[0])

#create and return a sleep tag        
def createDelay(value):
    delya_tag = etree.Element("delay")
    delya_tag.text = str(value)
    return delya_tag

#remove backup and forward tags from measures after serving their purpose
def removeShifts(measure):
    for elt in measure:
        if elt.tag=="backup" or elt.tag=="forward":
            measure.remove(elt)

#remove chord tag from notes
def removeChordTag(measure):
    chord_location = containsChord(measure)
    for i in range(len(measure)):
        if chord_location[i]:
            measure[i].remove(measure[i].xpath("chord")[0])
            
#return list containing each note and the time delay (in note durations) to play it
def parallelNotes(measure):
    time_delay = 0
    timed_note = list()
    chord_location = containsChord(measure)
    for i,elt in enumerate(measure):
        if elt.tag=="backup":
            time_delay = time_delay - int(elt.xpath("duration")[0].text)
        if elt.tag=="forward":
            time_delay = time_delay + int(elt.xpath("duration")[0].text)
        if elt.tag=="note" or elt.tag=="rest":
            timed_note.append([time_delay,elt])
            if i < len(chord_location)-1 and not(chord_location[i+1]):
                time_delay = time_delay + int(elt.xpath("duration")[0].text)
    return timed_note
    
#create delay tag in note and insert its value calculated from parallelNotes
def timedMeasure(measure):
    #ordering them serves no purpose
    #ordered_elts = sorted(parallelNotes(measure),key=lambda x: x[0])
    ordered_elts = parallelNotes(measure)
    removeShifts(measure)
    removeChordTag(measure)
    for i in ordered_elts:
        i[1].insert(-1,createDelay(i[0]))
        
def cleanMXL(root):
    #get list of measures
    simplifyScore(root)
    measures = root.xpath("part/measure")
    for measure in measures:
        clean(measure)
        createRest(measure)
        simplifyNote(measure)
        timedMeasure(measure)
    return root

def main():
    if len(sys.argv)==1:
        raise Exception("error: no argument passed")
    if len(sys.argv)>2:
        raise Exception("error: too many arguments")
    if ".xml" not in sys.argv[1]:
        raise Exception("error: wrong file extension")
    fname = sys.argv[1]
    print(fname)
    #read file and get the root head
    tree = etree.parse(fname)
    root = tree.getroot()

    cleanMXL(root)
    saveFile(root)

main()
