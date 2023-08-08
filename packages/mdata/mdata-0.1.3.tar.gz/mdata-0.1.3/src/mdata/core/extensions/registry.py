from mdata.core.util import StringEnumeration

CSV_KEY = 'extensions'

ExtensionTypeType = str


class Extensions(StringEnumeration):
    Metadata = 'metadata'
    Segmentation = 'segmentation'
    Annotations = 'annotations'


Extension = Extensions.derive_enum()
