import re
import javalang
import os
import pandas as pd
import json


def remove_fqdm(tokens, flg):
    tokens = list(tokens)
    result = []
    for t in tokens:
        if len(result) >= 4 and result[-1].value == '.' and result[-3].value == '.':
            result = result[:-4]+result[-2:]
            result.append(t)
        else:
            result.append(t)

    final_res = []
    flag = False
    for i, j in zip(result[:-1], result[1:]):
        if (i.value == 'lang' or i.value == 'util') and j.value == '.':
            flag = True
            continue
        else:
            if flag:
                flag = False
                continue
            else:
                final_res.append(i)

    retval = ' '.join([_.value for _ in final_res])
    if flg:
        retval += ';'
    return retval


def simplify(line):
    line = line.strip()
    flg = False
    if line.endswith(';'):
        flg = True
    if not line.endswith(';'):
        line += ';'
    tokens = javalang.tokenizer.tokenize(line)
    newline = remove_fqdm(tokens, flg)
    return newline


code = '''class X {
    encode(){
        org.junit.Assert.assertEquals(a.b.c.D.E, parsed);
        if(org.eclipse.xtext.xbase.lib.IterableExtensions.isNullOrEmpty(tokens)){return"";} 
        java.nio.ByteBuffer buffer=java.nio.ByteBuffer.allocate((((com.google.common.collect.Iterables.size(tokens))*2)*4));
        for(org.eclipse.lsp4j.util.SemanticHighlightingTokens.Token token:tokens){
            int character=token.character;int length=token.length;
            int scope=token.scope;
            int lengthAndScope=length;
            lengthAndScope=lengthAndScope<<(org.eclipse.lsp4j.util.SemanticHighlightingTokens.LENGTH_SHIFT); 
            lengthAndScope|=scope;buffer.putInt(character); 
            buffer.putInt(lengthAndScope); 
        }
        org . junit . Assert . assertEquals ( software . amazon . awssdk . protocols . json . AwsJsonErrorMessageParserTest . MESSAGE_CONTENT , parsed );
        assertEquals( a.b.c.D.E, parsed);
        return java.util.Base64.getEncoder().encodeToString(buffer.array());
    }
}
'''

with open('12-26-error.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

error_idx = [int(x) for x in data]
print(len(error_idx))

with open('input/Testing/assertLines.txt', 'r', encoding='utf-8') as f, open('input/Testing/testMethods.txt', 'r', encoding='utf-8') as g:
    alines = f.readlines()
    tlines = g.readlines()

output_data = []

for idx in error_idx:
    aline = alines[idx]
    tline = tlines[idx]
    output_data.append(
        {
            "line_number": idx+1,
            "assertLine": aline.strip(),
            "simplified_assertLine": simplify(aline.strip()),
            "testMethod": tline.strip(),
            "simplified_test_method": simplify(tline.strip())
        }
    )

with open('12-26-missing4k-lines.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=4)

output_data = []
for idx, (aline, tline) in enumerate(zip(alines, tlines)):
    if idx in error_idx:
        output_data.append(
            {
                "line_number": idx+1,
                "assertLine": aline.strip(),
                "simplified_assertLine": simplify(aline.strip()),
                "testMethod": tline.strip(),
                "simplified_test_method": simplify(tline.strip())
            }
        )

with open('12-26-missing-lines.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, indent=4)
