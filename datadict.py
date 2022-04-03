
# Example
# {
# 'groupname':xxx,
# 'members': [
#   {
#       'id':xxx,
#       'type':xxx,
#       'elements':[
#           {
#               'label':xxx,
#               'val':xxx
#           }
#          ]
#   },
#
#   ]
# }

# member types
# 'hdr' = elements in array with a text header (extra 'text' entry necessary)
# 'nhdr' = elements in array with no header
# '' = 

sensor_dict = {
    'groupname':'Joystick',
    'members': [
        {
            'id':'axispair',
            'type':'hdr',
            'text':'Thumbsticks',
            'elements':[
                {
                    'label':xxx,
                    'val':xxx
                },
            ]
        },
    ]
}


sensor_dict = {
    'groupname':'Joystick',
    'members': [
        {
            'id':'axispair',
            'type':'hdr',
            'text':'Thumbsticks',
            'elements':[
                {
                    'label':xxx,
                    'val':xxx
                },
            ]
        },
    ]
}


P3DX_robot_config = {
    'name':'',
    'states':[
        {
            'id':,
            'settings':[
                'interface':{
                    'groups':[
                        {
                            'name':'steering',
                            'label':'Joystick and Drive Motors',
                            'content':[   
                                InterfaceObject('left-joy','Stat 1',value=3,          display_round=None),
                                InterfaceObject('right-joy-y','right joy-y',value=0.444444,   display_round=5),
                                InterfaceObject('right-joy-y','right joy-y',value=0.444444,   display_round=5),
                                InterfaceObject('right-joy-y','right joy-y',value=0.444444,   display_round=5),
                                InterfaceObject('left-motor','Left motor',value=0.000003333,display_round=8),
                                InterfaceObject('right-motor','Right motor',value=3,          display_round=2),
    ]
                        }
                    ]
                }
            ]
        }
    ]
}
