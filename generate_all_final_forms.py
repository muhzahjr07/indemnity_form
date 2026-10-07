import os
import shutil
import zipfile
import struct
import re
import datetime
import xml.etree.ElementTree as ET

TEMPLATE_PATH = "Spillburg_Holdings_Indemnity_Form.docx"
FINAL_DIR = "final"

ALL_NS = {
    'wpc': 'http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas',
    'cx': 'http://schemas.microsoft.com/office/drawing/2014/chartex',
    'cx1': 'http://schemas.microsoft.com/office/drawing/2015/9/8/chartex',
    'cx2': 'http://schemas.microsoft.com/office/drawing/2015/10/21/chartex',
    'cx3': 'http://schemas.microsoft.com/office/drawing/2016/5/9/chartex',
    'cx4': 'http://schemas.microsoft.com/office/drawing/2016/5/10/chartex',
    'cx5': 'http://schemas.microsoft.com/office/drawing/2016/5/11/chartex',
    'cx6': 'http://schemas.microsoft.com/office/drawing/2016/5/12/chartex',
    'cx7': 'http://schemas.microsoft.com/office/drawing/2016/5/13/chartex',
    'cx8': 'http://schemas.microsoft.com/office/drawing/2016/5/14/chartex',
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
    'aink': 'http://schemas.microsoft.com/office/drawing/2016/ink',
    'am3d': 'http://schemas.microsoft.com/office/drawing/2017/model3d',
    'o': 'urn:schemas-microsoft-com:office:office',
    'oel': 'http://schemas.microsoft.com/office/2019/extlst',
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',
    'v': 'urn:schemas-microsoft-com:vml',
    'wp14': 'http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing',
    'wp': 'http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing',
    'w10': 'urn:schemas-microsoft-com:office:word',
    'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main',
    'w14': 'http://schemas.microsoft.com/office/word/2010/wordml',
    'w15': 'http://schemas.microsoft.com/office/word/2012/wordml',
    'w16cex': 'http://schemas.microsoft.com/office/word/2018/wordml/cex',
    'w16cid': 'http://schemas.microsoft.com/office/word/2016/wordml/cid',
    'w16': 'http://schemas.microsoft.com/office/word/2018/wordml',
    'w16du': 'http://schemas.microsoft.com/office/word/2023/wordml/word16du',
    'w16sdtdh': 'http://schemas.microsoft.com/office/word/2020/wordml/sdtdatahash',
    'w16sdtfl': 'http://schemas.microsoft.com/office/word/2024/wordml/sdtformatlock',
    'w16se': 'http://schemas.microsoft.com/office/word/2015/wordml/symex',
    'wpg': 'http://schemas.microsoft.com/office/word/2010/wordprocessingGroup',
    'wpi': 'http://schemas.microsoft.com/office/word/2010/wordprocessingInk',
    'wne': 'http://schemas.microsoft.com/office/word/2006/wordml',
    'wps': 'http://schemas.microsoft.com/office/word/2010/wordprocessingShape',
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
    'a14': 'http://schemas.microsoft.com/office/drawing/2010/main',
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',
}

for prefix, uri in ALL_NS.items():
    ET.register_namespace(prefix, uri)

def get_image_dimensions(filepath):
    try:
        with open(filepath, 'rb') as f:
            data = f.read()
            if data.startswith(b'\xff\xd8'):
                idx = 2
                while idx < len(data):
                    marker, = struct.unpack('>H', data[idx:idx+2])
                    idx += 2
                    if marker in (0xFFC0, 0xFFC2):
                        h, w = struct.unpack('>HH', data[idx+3:idx+7])
                        return w, h
                    else:
                        idx += struct.unpack('>H', data[idx:idx+2])[0]
            elif data.startswith(b'\x89PNG\r\n\x1a\n'):
                w, h = struct.unpack('>II', data[16:24])
                return w, h
    except Exception:
        pass
    return 400, 200

def make_run(text, font="Calibri", sz=20, bold=False, underline=False, superscript=False, space_preserve=False):
    r = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
    rPr = ET.SubElement(r, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
    
    rFonts = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
    rFonts.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ascii'] = font
    rFonts.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsi'] = font
    rFonts.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cs'] = font
    rFonts.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}asciiTheme'] = "majorHAnsi"
    rFonts.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsiTheme'] = "majorHAnsi"
    rFonts.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cstheme'] = "majorHAnsi"
    
    if sz:
        sz_el = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sz')
        sz_el.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'] = str(sz)
        szCs_el = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}szCs')
        szCs_el.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'] = str(sz)
        
    if bold:
        ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}b')
        
    if underline:
        u_el = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}u')
        u_el.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'] = "single"

    if superscript:
        va = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}vertAlign')
        va.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'] = "superscript"
        
    t = ET.SubElement(r, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t')
    if space_preserve or text.startswith(' ') or text.endswith(' '):
        t.attrib['{http://www.w3.org/XML/1998/namespace}space'] = 'preserve'
    t.text = text
    return r

def capitalize_address_words(text):
    if text.strip().lower() in ('local address', 'foreign address'):
        return 'Local Address' if 'local' in text.lower() else 'Foreign Address'
    
    clean = re.sub(r',\s*,+', ',', text)
    clean = re.sub(r'\s+', ' ', clean).strip()
    
    always_upper = {
        'USA', 'UK', 'CA', 'PB', 'HMT', 'PO', 'P.O.', 'II', 'III', 'IV', 'VI', 'VII', 'VIII', 'N.T.', 'EDF'
    }
    
    def cap_word(match):
        w = match.group(0)
        
        m_ord = re.match(r'^(\d+)(st|nd|rd|th)$', w, re.I)
        if m_ord:
            return m_ord.group(1) + m_ord.group(2).lower()
            
        m_floor = re.match(r'^(\d+)/([A-Za-z])$', w, re.I)
        if m_floor:
            return m_floor.group(1) + '/' + m_floor.group(2).upper()
            
        if re.match(r'^(?:[A-Z]{1,2}\d{1,2}[A-Z]?|\d[A-Z]{2})$', w, re.I):
            return w.upper()
            
        if w.upper() in always_upper:
            return w.upper()
            
        if re.match(r'^(?:VI|VII|VIII|IX|X)/\d+', w, re.I):
            return w.upper()
            
        if "'" in w:
            parts = w.split("'")
            return parts[0].capitalize() + "'" + parts[1].lower()
            
        return w.capitalize()

    result = re.sub(r"[A-Za-z0-9]+(?:'[A-Za-z]+)?", cap_word, clean)
    return result


def make_paragraph(runs):
    p = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
    pPr = ET.SubElement(p, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
    rPr = ET.SubElement(pPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
    rf = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
    rf.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}asciiTheme'] = "majorHAnsi"
    rf.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsiTheme'] = "majorHAnsi"
    rf.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cstheme'] = "majorHAnsi"
    
    for r in runs:
        p.append(r)
    return p

def make_drawing(r_id, pic_id, pic_num, img_path, target_max_width_emu=1150000, target_max_height_emu=500000):
    img_w, img_h = get_image_dimensions(img_path)
    aspect = (img_w / img_h) if img_h > 0 else 2.0
    cx = target_max_width_emu
    cy = int(cx / aspect)
    if cy > target_max_height_emu:
        cy = target_max_height_emu
        cx = int(cy * aspect)
        
    drawing_xml = f"""<w:drawing xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"
               xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"
               xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing"
               xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
               xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture"
               xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
               xmlns:a14="http://schemas.microsoft.com/office/drawing/2010/main">
      <wp:inline distT="0" distB="0" distL="0" distR="0" wp14:anchorId="350C0D15" wp14:editId="2A5EBE9D">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{pic_id}" name="Picture {pic_num}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic>
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic>
              <pic:nvPicPr>
                <pic:cNvPr id="0" name="Picture {pic_num}"/>
                <pic:cNvPicPr>
                  <a:picLocks noChangeAspect="1" noChangeArrowheads="1"/>
                </pic:cNvPicPr>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{r_id}">
                  <a:extLst>
                    <a:ext uri="{{28A0092B-C50C-407E-A947-70E740481C1C}}">
                      <a14:useLocalDpi val="0"/>
                    </a:ext>
                  </a:extLst>
                </a:blip>
                <a:srcRect/>
                <a:stretch>
                  <a:fillRect/>
                </a:stretch>
              </pic:blipFill>
              <pic:spPr bwMode="auto">
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{cx}" cy="{cy}"/>
                </a:xfrm>
                <a:prstGeom prst="rect">
                  <a:avLst/>
                </a:prstGeom>
                <a:noFill/>
                <a:ln>
                  <a:noFill/>
                </a:ln>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>"""
    return ET.fromstring(drawing_xml.strip())

def make_cell(width_dxa=1656, paragraphs=None, top_bot_mar=70, left_right_mar=70):
    tc = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tc')
    tcPr = ET.SubElement(tc, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcPr')
    
    tcW = ET.SubElement(tcPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcW')
    tcW.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w'] = str(width_dxa)
    tcW.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type'] = 'dxa'
    
    tcMar = ET.SubElement(tcPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tcMar')
    for m, val in [('top', top_bot_mar), ('left', left_right_mar), ('bottom', top_bot_mar), ('right', left_right_mar)]:
        node = ET.SubElement(tcMar, f'{{http://schemas.openxmlformats.org/wordprocessingml/2006/main}}{m}')
        node.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}w'] = str(val)
        node.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}type'] = 'dxa'
        
    vAlign = ET.SubElement(tcPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}vAlign')
    vAlign.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'] = 'center'
    
    if paragraphs:
        for p in paragraphs:
            tc.append(p)
    else:
        p = ET.SubElement(tc, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p')
        pPr = ET.SubElement(p, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}pPr')
        rPr = ET.SubElement(pPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
        rf = ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rFonts')
        rf.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}asciiTheme'] = "majorHAnsi"
        rf.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}hAnsiTheme'] = "majorHAnsi"
        rf.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cstheme'] = "majorHAnsi"
        
    return tc

def make_table_row(cells, tr_height=605):
    tr = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}tr')
    trPr = ET.SubElement(tr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}trPr')
    if tr_height:
        h = ET.SubElement(trPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}trHeight')
        h.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'] = str(tr_height)
    jc = ET.SubElement(trPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}jc')
    jc.attrib['{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val'] = 'center'
    
    for c in cells:
        tr.append(c)
    return tr

def build_date_runs(day, ordinal, month_year, sz=20, uppercase=False):
    ord_text = ordinal.upper() if uppercase else ordinal.lower()
    my_text = f" {month_year.upper() if uppercase else month_year}"
    return [
        make_run(str(day), sz=sz),
        make_run(ord_text, sz=sz, superscript=True),
        make_run(my_text, sz=sz, space_preserve=True)
    ]

def get_ordinal(d):
    if 11 <= (d % 100) <= 13:
        return 'th'
    return {1: 'st', 2: 'nd', 3: 'rd'}.get(d % 10, 'th')

def compute_dates(year, month, day):
    incorp_date = datetime.date(year, month, day)
    signing_date = incorp_date + datetime.timedelta(days=7)
    return {
        'incorp_day': str(incorp_date.day),
        'incorp_ord': get_ordinal(incorp_date.day).upper(),
        'incorp_month_year': incorp_date.strftime('%b %Y').upper(),
        'signing_day': str(signing_date.day),
        'signing_ord': get_ordinal(signing_date.day).lower(),
        'signing_month_year': signing_date.strftime('%b %Y'),
    }

def generate_document(company, is_signed, out_path):
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    
    with zipfile.ZipFile(TEMPLATE_PATH) as z:
        file_map = {name: z.read(name) for name in z.namelist()}
        
    orig_doc_bytes = file_map['word/document.xml']
    orig_header = orig_doc_bytes[:orig_doc_bytes.find(b'<w:body>')]
    
    # Ensure header has namespaces for drawingml
    header_str = orig_header.decode('utf-8')
    for p, uri in [
        ('a', 'http://schemas.openxmlformats.org/drawingml/2006/main'),
        ('a14', 'http://schemas.microsoft.com/office/drawing/2010/main'),
        ('pic', 'http://schemas.openxmlformats.org/drawingml/2006/picture')
    ]:
        if f'xmlns:{p}=' not in header_str:
            idx = header_str.rfind('>')
            header_str = header_str[:idx] + f' xmlns:{p}="{uri}"' + header_str[idx:]
    orig_header = header_str.encode('utf-8')

    doc_tree = ET.fromstring(orig_doc_bytes)
    tables = doc_tree.findall('.//w:tbl', ns)
    tbl1, tbl2, tbl3, tbl4 = tables[0], tables[1], tables[2], tables[3]
    
    media_files = {}
    rel_map = {}
    
    if is_signed:
        orig_ct = file_map['[Content_Types].xml'].decode('utf-8')
        orig_rels = file_map['word/_rels/document.xml.rels'].decode('utf-8')
        
        if 'Extension="jpeg"' not in orig_ct:
            orig_ct = orig_ct.replace('</Types>', '<Default Extension="jpeg" ContentType="image/jpeg"/><Default Extension="jpg" ContentType="image/jpeg"/><Default Extension="png" ContentType="image/png"/></Types>')
        
        # Collect distinct signature files from directors, shareholders, and signatory
        sig_files = []
        for d in company['directors']:
            sf = d.get('sig_file')
            if sf and os.path.exists(sf) and sf not in sig_files:
                sig_files.append(sf)
        for sh in company['shareholders']:
            sf = sh.get('sig_file')
            if sf and os.path.exists(sf) and sf not in sig_files:
                sig_files.append(sf)
        sf_signatory = company.get('signatory_sig')
        if sf_signatory and os.path.exists(sf_signatory) and sf_signatory not in sig_files:
            sig_files.append(sf_signatory)
            
        new_rels_str = ""
        for idx, sf in enumerate(sig_files):
            r_id = f"rId{11 + idx}"
            rel_map[sf] = r_id
            ext = os.path.splitext(sf)[1].lower()
            if ext in ('.jpg', '.jpeg'):
                target_ext = '.jpeg'
            elif ext == '.png':
                target_ext = '.png'
            else:
                target_ext = '.jpeg'
            target_name = f"media/image{idx+1}{target_ext}"
            media_files[f"word/{target_name}"] = sf
            new_rels_str += f'<Relationship Id="{r_id}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="{target_name}"/>'
            
        orig_rels = orig_rels.replace('</Relationships>', new_rels_str + '</Relationships>')
        file_map['[Content_Types].xml'] = orig_ct.encode('utf-8')
        file_map['word/_rels/document.xml.rels'] = orig_rels.encode('utf-8')

    # 1. Fill Table 1
    t1_rows = tbl1.findall('./w:tr', ns)
    
    # Row 1: Name of company - UPPERCASE Calibri size 10 (Rule 2)
    t1_r1_cell = t1_rows[0].findall('./w:tc', ns)[1]
    p = t1_r1_cell.find('./w:p', ns)
    p.clear()
    p.append(make_run(company['name'].upper(), sz=20))
    
    # Row 2: Company Registration No. - UPPERCASE Calibri size 10 (Rule 3)
    t1_r2_cell = t1_rows[1].findall('./w:tc', ns)[1]
    p = t1_r2_cell.find('./w:p', ns)
    p.clear()
    p.append(make_run(company['reg_no'].upper(), sz=20))
    
    # Row 3: Registered Office - UPPERCASE Calibri size 10 (Rule 4)
    t1_r3_cell = t1_rows[2].findall('./w:tc', ns)[1]
    p = t1_r3_cell.find('./w:p', ns)
    p.clear()
    p.append(make_run(company['office'].upper(), sz=20))
    
    # Row 4: Relevant instruction / filing / transaction (if any) - ALL (Rule 5)
    t1_r4_cell = t1_rows[3].findall('./w:tc', ns)[1]
    p = t1_r4_cell.find('./w:p', ns)
    p.clear()
    p.append(make_run(company['instruction'].upper(), sz=20))
    
    # Row 5: Effective Date - Incorp date UPPERCASE with superscript (Rule 6)
    t1_r5_cell = t1_rows[4].findall('./w:tc', ns)[1]
    p = t1_r5_cell.find('./w:p', ns)
    p.clear()
    for r in build_date_runs(company['incorp_day'], company['incorp_ord'], company['incorp_month_year'], sz=20, uppercase=True):
        p.append(r)
        
    # 2. Fill Table 2 (Directors)
    t2_rows = tbl2.findall('./w:tr', ns)
    for row in t2_rows[1:]:
        tbl2.remove(row)
        
    pic_counter = 1
    docpr_id = 650000000
    
    for d in company['directors']:
        c1_p = make_paragraph([make_run(d['name'].upper(), sz=20)])
        c1 = make_cell(1644, [c1_p])
        
        c2_paras = []
        for line in d['id_lines']:
            c2_paras.append(make_paragraph([make_run(line, sz=20)]))
        c2 = make_cell(1563, c2_paras if c2_paras else [make_paragraph([])])
        
        c3_paras = []
        for addr_line in d['address_paragraphs']:
            trimmed = addr_line.strip()
            if trimmed.lower() in ('local address', 'foreign address'):
                title = 'Local Address' if 'local' in trimmed.lower() else 'Foreign Address'
                c3_paras.append(make_paragraph([make_run(title, sz=18, bold=True, underline=True)]))
            else:
                c3_paras.append(make_paragraph([make_run(capitalize_address_words(trimmed), sz=18, bold=False, underline=False)]))
        c3 = make_cell(1626, c3_paras if c3_paras else [make_paragraph([])])
        
        # Col 4: Signature (Rule 16: larger realistic size ~1,150,000 EMUs)
        if is_signed and d.get('sig_file') and d['sig_file'] in rel_map:
            r_id = rel_map[d['sig_file']]
            drawing_el = make_drawing(r_id, docpr_id + pic_counter, pic_counter, d['sig_file'], target_max_width_emu=1150000, target_max_height_emu=500000)
            pic_counter += 1
            r_draw = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
            rPr = ET.SubElement(r_draw, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
            ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}noProof')
            r_draw.append(drawing_el)
            c4 = make_cell(2060, [make_paragraph([r_draw])])
        else:
            c4 = make_cell(2060, [make_paragraph([])])
            
        # Col 5: Date (Rule 14: 7 days from incorp date)
        date_runs = build_date_runs(company['signing_day'], company['signing_ord'], company['signing_month_year'], sz=20)
        c5 = make_cell(1656, [make_paragraph(date_runs)])
        
        # Col 6: Witness
        c6 = make_cell(1656, [make_paragraph([])])
        
        tbl2.append(make_table_row([c1, c2, c3, c4, c5, c6]))
        
    # 1 empty spacer row in Table 2
    tbl2.append(make_table_row([
        make_cell(1644, [make_paragraph([])]),
        make_cell(1563, [make_paragraph([])]),
        make_cell(1626, [make_paragraph([])]),
        make_cell(2060, [make_paragraph([])]),
        make_cell(1656, [make_paragraph([])]),
        make_cell(1656, [make_paragraph([])])
    ]))

    # 3. Fill Table 3 (Shareholders) - (Rule 15: include signature and signed date)
    t3_rows = tbl3.findall('./w:tr', ns)
    for row in t3_rows[1:]:
        tbl3.remove(row)
        
    for sh in company['shareholders']:
        c1_p = make_paragraph([make_run(sh['name'].upper(), sz=20)])
        c1 = make_cell(1644, [c1_p])
        
        c2_paras = []
        for line in sh.get('id_lines', []):
            c2_paras.append(make_paragraph([make_run(line, sz=20)]))
        c2 = make_cell(1563, c2_paras if c2_paras else [make_paragraph([])])
        
        c3_paras = []
        for addr in sh.get('address_paragraphs', []):
            trimmed = addr.strip()
            if trimmed.lower() in ('local address', 'foreign address'):
                title = 'Local Address' if 'local' in trimmed.lower() else 'Foreign Address'
                c3_paras.append(make_paragraph([make_run(title, sz=18, bold=True, underline=True)]))
            else:
                c3_paras.append(make_paragraph([make_run(capitalize_address_words(trimmed), sz=18, bold=False, underline=False)]))
        c3 = make_cell(1626, c3_paras if c3_paras else [make_paragraph([])])
        
        # Col 4: Signature (Rule 15 & 16)
        if is_signed and sh.get('sig_file') and sh['sig_file'] in rel_map:
            r_id = rel_map[sh['sig_file']]
            drawing_el = make_drawing(r_id, docpr_id + pic_counter, pic_counter, sh['sig_file'], target_max_width_emu=1150000, target_max_height_emu=500000)
            pic_counter += 1
            r_draw = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
            rPr = ET.SubElement(r_draw, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
            ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}noProof')
            r_draw.append(drawing_el)
            c4 = make_cell(2060, [make_paragraph([r_draw])])
        else:
            c4 = make_cell(2060, [make_paragraph([])])
            
        # Col 5: Signed Date (Rule 15: same as company's signed date)
        if is_signed:
            date_runs = build_date_runs(company['signing_day'], company['signing_ord'], company['signing_month_year'], sz=20)
            c5 = make_cell(1656, [make_paragraph(date_runs)])
        else:
            c5 = make_cell(1656, [make_paragraph([])])
            
        # Col 6: Witness
        c6 = make_cell(1656, [make_paragraph([])])
        tbl3.append(make_table_row([c1, c2, c3, c4, c5, c6]))
        
    # Spacer row in Table 3
    tbl3.append(make_table_row([
        make_cell(1644, [make_paragraph([])]),
        make_cell(1563, [make_paragraph([])]),
        make_cell(1626, [make_paragraph([])]),
        make_cell(2060, [make_paragraph([])]),
        make_cell(1656, [make_paragraph([])]),
        make_cell(1656, [make_paragraph([])])
    ]))
    
    # 4. Fill Table 4 (Common Seal / Signatory)
    t4_rows = tbl4.findall('./w:tr', ns)
    
    # Row 1: Authorised Signatory / Director
    t4_r1_cell = t4_rows[0].findall('./w:tc', ns)[1]
    p = t4_r1_cell.find('./w:p', ns)
    p.clear()
    p.append(make_run(company['signatory_name'].upper(), sz=20))
    
    # Row 2: Signature and Date
    t4_r2_cell = t4_rows[1].findall('./w:tc', ns)[1]
    p = t4_r2_cell.find('./w:p', ns)
    p.clear()
    
    if is_signed and company.get('signatory_sig') and company['signatory_sig'] in rel_map:
        r_id = rel_map[company['signatory_sig']]
        drawing_el = make_drawing(r_id, docpr_id + pic_counter, pic_counter, company['signatory_sig'], target_max_width_emu=1050000, target_max_height_emu=450000)
        pic_counter += 1
        r_draw = ET.Element('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}r')
        rPr = ET.SubElement(r_draw, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr')
        ET.SubElement(rPr, '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}noProof')
        r_draw.append(drawing_el)
        p.append(r_draw)
        
    date_runs = build_date_runs(company['signing_day'], company['signing_ord'], company['signing_month_year'], sz=20)
    for r in date_runs:
        p.append(r)
        
    # Row 3: Company seal
    t4_r3_cell = t4_rows[2].findall('./w:tc', ns)[1]
    p = t4_r3_cell.find('./w:p', ns)
    p.clear()

    # Re-save document.xml preserving the original root tag and all 36 namespaces & mc:Ignorable declarations
    serialized = ET.tostring(doc_tree, encoding='utf-8')
    body_idx = serialized.find(b'<w:body>')
    if body_idx != -1:
        fixed_xml = orig_header + serialized[body_idx:]
    else:
        body_idx2 = serialized.find(b':body>')
        tag_start = serialized.rfind(b'<', 0, body_idx2)
        fixed_xml = orig_header + serialized[tag_start:]

    file_map['word/document.xml'] = fixed_xml
    
    # Write output docx
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as out_zip:
        for name, data in file_map.items():
            out_zip.writestr(name, data)
        for target_path, local_path in media_files.items():
            with open(local_path, 'rb') as f:
                out_zip.writestr(target_path, f.read())
                
    print(f"Generated: {out_path}")

try:
    from companies_catalog import ALL_COMPANIES
except ImportError:
    from companies_catalog_sample import ALL_COMPANIES

def main():
    print(f"Starting generation for {len(ALL_COMPANIES)} companies...")
    for idx, company in enumerate(ALL_COMPANIES, 1):
        comp_dir = os.path.join(FINAL_DIR, company['folder_name'])
        os.makedirs(comp_dir, exist_ok=True)
        
        draft_path = os.path.join(comp_dir, f"{company['file_prefix']}_draft.docx")
        signed_path = os.path.join(comp_dir, f"{company['file_prefix']}_signed.docx")
        
        generate_document(company, is_signed=False, out_path=draft_path)
        generate_document(company, is_signed=True, out_path=signed_path)
        print(f"[{idx}/{len(ALL_COMPANIES)}] Completed {company['name']}")
    print("\nAll indemnity forms generated successfully!")

if __name__ == '__main__':
    main()

