SyntaxHighlighter.brushes.Vhdl = function()
{
	var keywords =	'abs else label package then ' +
					'access elsif library port to ' +
					'after end linkage postponed transport ' +
					'alias entity literal procedure type ' +
					'all exit loop process ' +
					'and pure unaffected ' +
					'architecture file map units ' +
					'array for mod range until ' +
					'assert function record use ' +
					'attribute nand register ' +
					'generate new reject variable ' +
					'begin generic next rem ' +
					'block group nor report wait ' +
					'body guarded not return when ' +
					'buffer null rol while ' +
					'bus if ror with ' +
					'impure of ' +
					'case in on select xnor ' +
					'component inertial open severity xor ' +
					'configuration inout or shared ' +
					'constant is others ' +
					'out sla ' +
					'disconnect sll ' +
					'downto sra ' +
					'srl ' +
					'subtype';

	var functionnames =      'or\_reduce gate\_and gate\_xor';

	this.regexList = [
		{ regex: /\-\-\!\!.*$/gm,	                     				css: 'color2' },		// bugspray
		{ regex: /\-\-\#\#.*$/gm,									css: 'color3' },		// figtree
		{ regex: /\-\-\!.*$/gm,	css: 'comments' },		// comments with --!
		{ regex: /\-\-\*.*$/gm,	css: 'comments' },		// comments with --*
		{ regex: /\-\-.*$/gm,	css: 'color1' },		// normal comments with --
		{ regex: SyntaxHighlighter.regexLib.doubleQuotedString,		css: 'string' },		// strings
		{ regex: SyntaxHighlighter.regexLib.singleQuotedString,		css: 'string' },		// strings
		{ regex: /\b([\d]+(\.[\d]+)?|0x[a-f0-9]+)\b/gi,				css: 'value' },			// numbers
		{ regex: new RegExp(this.getKeywords(keywords), 'gmi'),		css: 'keyword' },		// vhdl keywords
		{ regex: new RegExp('signal', 'gmi'),							css: 'variable' },		// variable
		{ regex: new RegExp(this.getKeywords(functionnames), 'gmi'),		css: 'functions' }		// vhdl functions
		];

	this.forHtmlScript(SyntaxHighlighter.regexLib.aspScriptTags);
};

SyntaxHighlighter.brushes.Vhdl.prototype	= new SyntaxHighlighter.Highlighter();
SyntaxHighlighter.brushes.Vhdl.aliases		= ['vhdl'];
