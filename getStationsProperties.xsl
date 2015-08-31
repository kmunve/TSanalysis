<?xml version="1.0"?>

<xsl:stylesheet version="1.0"
xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="/">
 <html>
 <body>
   <h2>eklima stations</h2>
   <table border="1">
     <tr bgcolor="#9acd32">
       <th>Name</th>
       <th>Station ID</th>
       <th>Elevation</th>
       <th>Department</th>
     </tr>
     <xsl:for-each select="//return/item">
      <xsl:sort select="department"/>
      <xsl:if test="amsl &gt; 600">
       <tr>
         <td><xsl:value-of select="name"/></td>
         <td><xsl:value-of select="stnr"/></td>
         <td><xsl:value-of select="department"/></td>
         <td><xsl:value-of select="amsl"/></td>
       </tr>
      </xsl:if>
     </xsl:for-each>
   </table>
 </body>
 </html>
</xsl:template>

</xsl:stylesheet>
