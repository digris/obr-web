import { watch } from "vue";

import { useDevice } from "@/composables/device";
import { usePlayerControls, usePlayerState } from "@/composables/player";
import { useQueueControls } from "@/composables/queue";
import { getImageSrc } from "@/utils/image";

class MediaSessionHandler {
  session: MediaSession | null;

  pause = async (): Promise<void> => {};
  resume = async (): Promise<void> => {};
  playNext = async (): Promise<void> => {};
  playPrevious = async (): Promise<void> => {};

  constructor() {
    const { isWeb } = useDevice();
    const { media, isLive } = usePlayerState();
    const { pause: pauseFn, resume: resumeFn } = usePlayerControls();
    const { playNext: playNextFn, playPrevious: playPreviousFn } = useQueueControls();
    this.pause = pauseFn;
    this.resume = resumeFn;
    this.playNext = playNextFn;
    this.playPrevious = playPreviousFn;

    if ("mediaSession" in navigator && isWeb) {
      // @ts-ignore
      this.session = navigator.mediaSession;
      this.setupBindings(isLive.value);
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
    if (!this.session) {
      return;
    }

    if (isLive) {
      this.session.setActionHandler("pause", this.pause);
      this.session.setActionHandler("play", this.resume);
      this.session.setActionHandler("previoustrack", null);
      this.session.setActionHandler("nexttrack", null);
    } else {
      this.session.setActionHandler("pause", this.pause);
      this.session.setActionHandler("play", this.resume);
      this.session.setActionHandler("previoustrack", this.playPrevious);
      this.session.setActionHandler("nexttrack", this.playNext);
    }
  }

  setMetadata(media: any) {
    if (!(media && this.session)) {
      return;
    }

    // TODO: implement properly
    const release = media.releases.length ? media.releases[0] : null;
    // const artwork: { src: string | null; sizes: string; type: string }[] = [];
    const artwork: MediaImage[] = [];

    if (release && release.image) {
      const sizes = [96, 256];
      sizes.forEach((size) => {
        artwork.push({
          src: getImageSrc(release.image, size) || "",
          sizes: `${size}x${size}`,
          type: "image/png",
        });
      });
    }
    // console.debug("artwork", artwork);
    this.session.metadata = new MediaMetadata({
      title: media.name,
      artist: media.artistDisplay,
      album: release ? release.name : "-",
      artwork,
    });
  }
}

export default function () {
  return new MediaSessionHandler();
}
