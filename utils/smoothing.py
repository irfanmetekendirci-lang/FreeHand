# İmlecin titremeden ilk konumundan son konumuna düzeni ve kayarak gitmesini sağlayacağız
import config

# Lerp: İki sayı, renk veya konum arasında düz ve yumuşak bir geçiş yapmayı sağlar.
#       Genellikle üç girdi alır: başlangıç değeri (a), bitiş değeri (b) ve 0 ile 1 arasında bir oran
def lerp(first_loc, last_loc, smooth_value):
    return first_loc + (last_loc - first_loc) * smooth_value


def smooth_location(prev_x, prev_y, curr_x, curr_y, smooth_factor=0.25):        # prev_:previous = önceki, curr_:current = şu anki
    """
    Hem X hem Y koordinatı için Lerp uygular ve yumuşatılmış yeni koordinatları döner.
    """
    smooth_x = lerp(prev_x, curr_x, smooth_factor)
    smooth_y = lerp(prev_y, curr_y, smooth_factor)
    
    return smooth_x, smooth_y


