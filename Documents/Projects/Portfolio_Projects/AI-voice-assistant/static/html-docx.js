/*!
 * Simple HTML to RTF converter for Word export
 * Creates RTF files that can be opened in Microsoft Word
 */

(function() {
    var htmlDocx = (function() {
        
        function asBlob(htmlContent) {
            // Convert HTML to plain text and create RTF
            var plainText = htmlContent
                .replace(/<h1[^>]*>(.*?)<\/h1>/gi, '\\par \\b \\fs28 $1 \\b0 \\fs24 \\par ')
                .replace(/<h2[^>]*>(.*?)<\/h2>/gi, '\\par \\b \\fs24 $1 \\b0 \\par ')
                .replace(/<h[3-6][^>]*>(.*?)<\/h[3-6]>/gi, '\\par \\b $1 \\b0 \\par ')
                .replace(/<p[^>]*>(.*?)<\/p>/gi, '\\par $1 \\par ')
                .replace(/<br[^>]*>/gi, '\\par ')
                .replace(/<strong[^>]*>(.*?)<\/strong>/gi, '\\b $1 \\b0 ')
                .replace(/<b[^>]*>(.*?)<\/b>/gi, '\\b $1 \\b0 ')
                .replace(/<em[^>]*>(.*?)<\/em>/gi, '\\i $1 \\i0 ')
                .replace(/<i[^>]*>(.*?)<\/i>/gi, '\\i $1 \\i0 ')
                .replace(/<[^>]+>/g, '') // Remove remaining HTML tags
                .replace(/&nbsp;/g, ' ')
                .replace(/&amp;/g, '&')
                .replace(/&lt;/g, '<')
                .replace(/&gt;/g, '>')
                .replace(/&quot;/g, '"')
                .replace(/'/g, "'");
            
            // Create RTF document
            var rtfContent = '{\\rtf1\\ansi\\deff0 {\\fonttbl {\\f0 Times New Roman;}}\\f0\\fs24 ' + plainText + '}';
            
            return new Blob([rtfContent], {
                type: 'application/rtf'
            });
        }
        
        return {
            asBlob: asBlob
        };
    })();
    
    // Export to global scope
    if (typeof window !== 'undefined') {
        window.htmlDocx = htmlDocx;
    }
})();
