<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
 <html>
 <body>
   <h2>eklima stations</h2>
   <table border="1">
     <tr bgcolor="#9acd32">
       <th>Navn</th>
       <th>Stasjons ID</th>
       <th>Høyde</th>
       <th>Fylke</th>
       <th>År</th>
     </tr>
     <xsl:for-each select="//return/item">
      <xsl:sort select="fromYear"/>
      <!--<xsl:if test="amsl &gt; 600">-->
       <tr>
         <td><xsl:value-of select="name"/></td>
         <td><xsl:value-of select="stnr"/></td>
         <td><xsl:value-of select="department"/></td>
         <td><xsl:value-of select="amsl"/></td>
         <td><xsl:value-of select="fromYear"/></td>
       </tr>
     <!--</xsl:if>-->
     </xsl:for-each>
   </table>



<!--
   <script type="text/javascript" src="http://maps.google.com/maps/api/js?sensor=false">
   </script>
   <div style="overflow:hidden;height:500px;width:600px;">
     <div id="gmap_canvas" style="height:500px;width:600px;">
     </div>
     <style>#gmap_canvas img{max-width:none!important;background:none!important}
     </style>
     <a class="google-map-code" href="http://www.themecircle.net" id="get-map-data">themecircle
     </a>
   </div>
   <script type="text/javascript"> function init_map(){var myOptions = {zoom:14,center:new google.maps.LatLng(40.805478,-73.96522499999998),mapTypeId: google.maps.MapTypeId.ROADMAP};map = new google.maps.Map(document.getElementById("gmap_canvas"), myOptions);marker = new google.maps.Marker({map: map,position: new google.maps.LatLng(40.805478, -73.96522499999998)});infowindow = new google.maps.InfoWindow({content:"<b>The Breslin</b><br/>2880 Broadway<br/> New York" });google.maps.event.addListener(marker, "click", function(){infowindow.open(map,marker);});infowindow.open(map,marker);}google.maps.event.addDomListener(window, 'load', init_map);
 </script>
-->

 </body>
 </html>
</xsl:template>

</xsl:stylesheet>
