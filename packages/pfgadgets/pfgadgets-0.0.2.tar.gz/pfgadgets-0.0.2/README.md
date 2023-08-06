# pfgadgets package

Description: This package is designed to assist in the use of python within the powerfactory environment

## Classes List:
- CreateSet
- FrequencySweep
- GetData
- GetObject
- GetPlot
- HarmonicLoadFlow
- LoadFlow
- ShortCircuit

## Class Description
### pfgadgets.CreateSet
*__CreateSet(setName, *args, setType=5, studyCaseName=None)__*

*Description*: This class is designed to create a set

*Parameters*: 
- setName - Name of set to create
- setType - Defines the type of set to create. Refer PF for types
- studyCaseName - Defines the name of the study case to create set in. If None then will create in active study case

*Attributes*: 
- .set - Returns the created set object
---
### pfgadgets.FrequencySweep
*__FrequencySweep(*args, method=0, init=0, start=50, stop=2500, results=None)__*

*Description*: This class is designed to perform a frequency sweep calaculation

*Parameters*:
- method - defines the frequency sweep method (0 - balanced, 1 - unbalanced)
- init - defines whether to initialise with load flow
- start - defines the starting frequency
- stop - defines the ending frequency
- results - defines which results variable to save results to
---
### pfgadgets.GetData
*__GetData(setName, attributeList, *args, resultHeadings=None)__*

*Description*: This class is designed to collect data from a set and offers export to csv option

*Parameters*: 
- setName - Name of the set to extract data from
- attributeList - List of attributes to get data from
- resultHeadings - List of strings for data frame headings

*Attributes*: 
- .obj - Returns object/s that data was collected from
- .name - Returns name of object/s that data was collected from
- .attribute - Returns list of attributes that was collected
- .result - Returns the results data frame that holds the extracted data
---
### pfgadgets.GetData.export
*__pfgadgets.GetData.export(fileName = 'results', filePath =  None, replace=False)__*

*Description*: Exports the collected data to a csv

*Parameters*: 
- fileName - Name of file that data will export to. Should not include file extension.
- filePath - Defines directory where csv will export to. If None then export to script directory
- replace - Defines whether to replace existing files or not. (False - do not replace existing, True - replace existing)
---
### pfgadgets.GetObject
*__pfgadgets.GetObject(objectName)__*

*Description*: This class is deisnged to collect a given object

*Parameters*: 
- objectName - Name of object to collect

*Attributes*: 
- .obj - Returns the collected object
- .name - Returns the name of the collected object
---
### pfgadgets.GetPlot
*__pfgadgets.GetPlot(plotName, pageType='SetVipage')__*

*Description*: This class is designed to collect a plot page and offers an export option

*Parameters*: 
- plotName - Name of plot to be collected
- pageType - Defined the type of page to be collected
	
*Attributes*: 
- .plot - Returns to plot objects that was collected
- .title - Returns the title object that may be included in a plot page
---
### pfgadgets.GetPlot.export
*__pfgadgets.GetPlot.export(*args, fileType='wmf', filePath=None, frame = 0, fileName=None, replace=False)__*

*Description*: Exports the plot page to the desired type and location

*Parameters*: 
- fileType - Defines the extension of the exported plot page file
- filePath - Defines directory where csv will export to. If None then export to script directory
- frame - Defines whether to include a page fram or not (0 - no frame, 1 - include frame)
- fileName - Name of file that data will export to. Should not include file extension.
- replace - Defines whether to replace existing files or not. (False - do not replace existing, True - replace existing)
---
### pfgadgets.HarmonicLoadFlow
*__pfgadgets.HarmonicLoadFlow(*args, method=0)__*

*Description*: This class is designed to perform a harmonic load flow calcualtion

*Parameters*: 
- method - defines the harmonic load flow method (0 - balanced, 1 - unbalanced)
---
### pfgadgets.LoadFlow
*__pfgadgets.LoadFlow(method=0, autoTap=0, feederScaling=0, opScen=None)__*

*Description*: This class is designed to perform a load flow calculation

*Parameters*: 
- method - defines the load flow method (0 - balanced, 1 - unbalanced)
- autoTap - defines whether to enable automatic tap changine (0 - off, 1 - on)
- feederScaling - defines whether to enable feeder load scaling (0 - off, 1 - on)
- opScen - defines the operation scenario to activate before calculation (if None then then no operation sceanrio will be activated)
---
### pfgadgets.ShortCircuit
*__pfgadgets.ShortCircuit(objectName, faultType='3psc', calculate=0, setSelect=None, opScen=None)__*

*Description*: This class is designed to perform a short-circuit calculation

*Parameters*: 
- objectName - Name of object to perform short-circuit calculation on. If setSelect!=None then a set can be passed instead of an object
- faultType - Defines the type of fault to use during short-circuit calculation
- calculate - Defines whether to use maximum or minimum fault calculation (0 - maximum, 1 - minimum)
- setSelect - Defines whether a set or single object is used for calculation (None - single object, != None - set)

*Attributes*: 
- .obj - Returns object/s where short-circuit calculation was performed
- .name - Returns name/s of objects where short-circuit calculation was performed
