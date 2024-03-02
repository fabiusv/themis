def optional_unwrap(array: [any], subscripts: [str]):
    try:
        for i in subscripts:
            array = array[i]
    except:
        return None
    return array