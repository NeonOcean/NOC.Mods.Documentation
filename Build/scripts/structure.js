ChangeFlip = 0
ChangeExpand = 1
ChangeCollapse = 2

function LoadStructure () {
	CreateStructure(StructureIndexing, document.getElementById("Sidebar"), true);
	
	documentURLLower = window.location.pathname.substring(1).toLowerCase();
	documentURLLower = documentURLLower.replace(new RegExp("/+$"), "");
	
	documentLastSlashPosition = documentURLLower.lastIndexOf("/");
	documentName = documentURLLower.substring(documentLastSlashPosition + 1);
	documentName = documentName.substring(0, documentName.lastIndexOf("."));
	
	if(documentName == "index") {
		documentURLLower = documentURLLower.substring(0, documentLastSlashPosition);
	}
	
	linkElements = document.getElementById("Sidebar").getElementsByTagName("A");
	
	for(var linkElementIndex = 0; linkElementIndex < linkElements.length; linkElementIndex++) {
		if(linkElements[linkElementIndex].className == "Structure_Entry_Name") {
			
			linkURLLower = linkElements[linkElementIndex].pathname.substring(1).toLowerCase();
			linkURLLower = linkURLLower.replace(new RegExp("/+$"), "");
			
			linkLastSlashPosition = linkURLLower.lastIndexOf("/");
			linkName = linkURLLower.substring(linkLastSlashPosition + 1);
			linkName = linkName.substring(0, linkName.lastIndexOf("."));
			
			if(linkName == "index") {
				linkURLLower = linkURLLower.substring(0, linkLastSlashPosition);
			}
			
			if(linkURLLower == documentURLLower) {
				StructureChangeCurrentDocument(linkElements[linkElementIndex]);
				linkElements[linkElementIndex].setAttribute("style", "color: crimson; font-weight: bold;");
				break;
			}
		}
	}
}

function CreateStructure (structure, containingElement, isRoot) {
	var listElement = document.createElement("ul");
	listElement.className = "Structure_List";
		
	if(!isRoot) {
		listElement.style.display = "none";
	}
	
	for(var structureIndex = 0; structureIndex < structure.length; structureIndex++) {
		var entryElement = document.createElement("li");
		entryElement.className = "Structure_Entry";
		
		var entryExpanderElement = document.createElement("div");
		
		if("Entries" in structure[structureIndex]) {
			entryExpanderElement.className = "Structure_Entry_Expander_Collapsed";
			entryExpanderElement.onclick = StructureFlipExpanderElementEvent;
		} else {
			entryExpanderElement.className = "Structure_Entry_Expander_Hidden";
		}
		
		if("Path" in structure[structureIndex]) {
			var entryNameElement = document.createElement("a");
			entryNameElement.href = structure[structureIndex]["Path"];
		} else {
			var entryNameElement = document.createElement("span");
			entryNameElement.onclick = StructureFlipNameElementEvent;
		}
		
		entryNameElement.className = "Structure_Entry_Name";
		
		if("Name" in structure[structureIndex]) {
			entryNameElement.innerHTML = structure[structureIndex]["Name"];
		} else {
			entryNameElement.innerHTML = "Error: Unknown name";
		}
		
		entryElement.appendChild(entryExpanderElement);
		entryElement.appendChild(entryNameElement);
		
		listElement.appendChild(entryElement);
		
		if("Entries" in structure[structureIndex]) {
			CreateStructure(structure[structureIndex]["Entries"], entryElement, false);
			
			if("StartOpened" in structure[structureIndex]) {
				if(structure[structureIndex]["StartOpened"]) {
					StructureChangeExpanderElement(entryExpanderElement, ChangeExpand);
				}
			}
		}
	}
	
	containingElement.appendChild(listElement);
}

function StructureChangeCurrentDocument (nameElement) {
	if(nameElement.parentElement != null && nameElement.parentElement.className == "Structure_Entry") {
		StructureChangeEntryElementRecursive(nameElement.parentElement, ChangeExpand);
	}
	
	nameElement.scrollIntoView(true)
}

function StructureChangeEntryElement (entryElement, changeType) {
	for(var childNodeIndex = 0; childNodeIndex < entryElement.childNodes.length; childNodeIndex++) {
		if(entryElement.childNodes[childNodeIndex].className == "Structure_Entry_Expander_Expanded" ||
			entryElement.childNodes[childNodeIndex].className == "Structure_Entry_Expander_Collapsed") {
			StructureChangeExpanderElement(entryElement.childNodes[childNodeIndex], changeType);
			break;
		}
	}
}

function StructureChangeEntryElementRecursive (entryElement, changeType) {
	StructureChangeEntryElement(entryElement, changeType);
	
	if(entryElement.parentElement != null && entryElement.parentElement.className == "Structure_List") {
		if(entryElement.parentElement.parentElement != null && entryElement.parentElement.parentElement.className == "Structure_Entry") {
			StructureChangeEntryElementRecursive(entryElement.parentElement.parentElement, changeType);
		}
	}
}

function StructureChangeNameElement (nameElement, changeType) {
	if(nameElement.parentElement != null && nameElement.parentElement.className == "Structure_Entry") {
		StructureChangeEntryElement(nameElement.parentElement, changeType);
	}
}

function StructureChangeNameElementRecursive (nameElement, changeType) {
	if(nameElement.parentElement != null && nameElement.parentElement.className == "Structure_Entry") {
		StructureChangeEntryElementRecursive(nameElement.parentElement, changeType);
	}
}

function StructureChangeExpanderElement (expanderElement, changeType) {
	if(expanderElement.className == "Structure_Entry_Expander_Collapsed" && (changeType == ChangeExpand || changeType == ChangeFlip))  {
		expanderElement.className = "Structure_Entry_Expander_Expanded";
		
		for(var childNodeIndex = 0; childNodeIndex < expanderElement.parentElement.childNodes.length; childNodeIndex++) {
			if(expanderElement.parentElement.childNodes[childNodeIndex].nodeName == "UL") {
				expanderElement.parentElement.childNodes[childNodeIndex].style.display = "block";
			}
		}
	} else if(expanderElement.className == "Structure_Entry_Expander_Expanded" && (changeType == ChangeCollapse || changeType == ChangeFlip)) {
		expanderElement.className = "Structure_Entry_Expander_Collapsed";
		
		for(var childNodeIndex = 0; childNodeIndex < expanderElement.parentElement.childNodes.length; childNodeIndex++) {
			if(expanderElement.parentElement.childNodes[childNodeIndex].nodeName == "UL") {
				expanderElement.parentElement.childNodes[childNodeIndex].style.display = "none";
			}
		}
	}
}

function StructureFlipEntryElementEvent () {
	StructureChangeEntryElement(this, ChangeFlip);
}

function StructureFlipNameElementEvent () {
	StructureChangeNameElement(this, ChangeFlip);
}

function StructureFlipExpanderElementEvent () {
	StructureChangeExpanderElement(this, ChangeFlip);
}

window.addEventListener("load", LoadStructure);
