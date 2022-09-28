import { ref } from "vue";
import eventBus from "@/eventBus";
import settings from "@/settings";
import { usePlayerState } from "@/composables/player";
import { getImageSrc } from "@/utils/image";
import { watch } from "vue";

class MediaSessionHandler {
  session: null;

  constructor() {
    // TODO: fix for pinia
    // const { isLive, media } = usePlayerState();
    const { isLive } = usePlayerState();
    // const isLive = ref(false);
    const media = ref(null);
    if ("mediaSession" in navigator && settings.CLIENT_MODE_APP === "web") {
      // @ts-ignore
      this.session = navigator.mediaSession;
      this.setupBindings(true);
      watch(
        () => media.value,
        (value) => {
          this.setMetadata(value);
          this.setupBindings(isLive.value);
        }
      );
    } else {
      this.session = null;
    }
  }

  setupBindings(isLive: boolean) {
    // @ts-ignore
    this.session.setActionHandler("pause", () => {
      eventBus.emit("player:controls", { do: "pause" });
    });
    if (isLive) {
      // @ts-ignore
      this.session.setActionHandler("previoustrack", null);
      // @ts-ignore
      this.session.setActionHandler("nexttrack", null);
    } else {
      // @ts-ignore
      this.session.setActionHandler("previoustrack", () => {
        eventBus.emit("queue:controls:playPrevious");
      });
      // @ts-ignore
      this.session.setActionHandler("nexttrack", () => {
        eventBus.emit("queue:controls:playNext");
      });
    }
  }

  setMetadata(media: any) {
    if (!media) {
      return;
    }
    const release = media.releases.length ? media.releases[0] : null;
    const artwork: { src: string | null; sizes: string; type: string }[] = [];
    if (release && release.image) {
      const sizes = [96, 256];
      sizes.forEach((size) => {
        artwork.push({
          src: getImageSrc(release.image, size),
          sizes: `${size}x${size}`,
          type: "image/png",
        });
      });
    }
    // @ts-ignore
    this.session.metadata = new MediaMetadata({
      title: media.name,
      artist: media.artistDisplay,
      album: release ? release.name : "-",
      // @ts-ignore
      artwork,
    });
  }
}

export default function () {
  return new MediaSessionHandler();
}
