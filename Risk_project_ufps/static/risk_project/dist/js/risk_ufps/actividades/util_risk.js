
/*
 * Convierte un archivo file de tipo xml a un json
 */
function obtenerJson(file_xml, _callback){	
	if (file_xml) {
	    var reader = new FileReader();
	    reader.readAsText(file_xml, "UTF-8");
	    reader.onload = function (evt) {
			var my_dom = parseXml(evt.target.result);
			var my_json = xml2json(my_dom, ""); 	 		
			_callback(JSON.parse(my_json));	
	    }

	    reader.onerror = function (evt) {
	    	my_json = { "error" : evt.target.error };	
	    	_callback(JSON.parse(my_json));		        
	    }
	}

}

/*
*	Convierte una cadena de texto en xml
*/
function parseXml(xml) {
   var dom = null;
   if (window.DOMParser) {
      try { 
         dom = (new DOMParser()).parseFromString(xml, "text/xml"); 
      } 
      catch (e) { dom = null; }
   }
   else if (window.ActiveXObject) {
      try {
         dom = new ActiveXObject('Microsoft.XMLDOM');
         dom.async = false;
         if (!dom.loadXML(xml)) // parse error ..

            window.alert(dom.parseError.reason + dom.parseError.srcText);
      } 
      catch (e) { dom = null; }
   }
   else
      alert("cannot parse xml string!");
   return dom;
}
	